"""Build a reproducible plugin archive and complete static website payload."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def package_files(root):
    plugin = root / "voiceflow"
    for path in sorted(plugin.rglob("*")):
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            raise ValueError("Symlinks cannot be published")
        if path.is_file():
            yield path.relative_to(root).as_posix(), path.read_bytes()


def rewrite_setup(text, source, root):
    """Only rewrite inline Markdown links outside code fences."""
    lines = []
    is_fenced = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith(("```", "~~~")):
            is_fenced = not is_fenced
        elif not is_fenced:
            def replace(match):
                link = match.group(2)
                if "://" in link or link.startswith("#"):
                    return match.group(0)
                path, separator, fragment = link.partition("#")
                target = (source.parent / path).resolve()
                if not target.is_relative_to((root / "voiceflow").resolve()) or not target.is_file():
                    raise ValueError(f"Invalid publication link: {link}")
                relative = target.relative_to(root.resolve()).as_posix()
                return match.group(1) + relative + (separator + fragment if separator else "") + ")"
            line = re.sub(r"(\[[^\]]*\]\()([^\s)]+)\)", replace, line)
        lines.append(line)
    return "".join(lines)


def build(root=ROOT, output=None):
    root = root.resolve()
    output = (output or root / "dist").resolve()
    # Only this generated directory is replaced; don't accept arbitrary deletion targets.
    if output != root / "dist":
        raise ValueError("Output must be the repository's dist directory")
    if output.is_symlink():
        raise ValueError("Output symlink refused")
    if output.exists():
        shutil.rmtree(output)
    site = output / "site/agents"
    site.mkdir(parents=True)
    files = list(package_files(root))
    for name, data in files:
        target = site / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    archive = site / "voiceflow.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for name, data in files:
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            bundle.writestr(entry, data)
    guide = root / "voiceflow/skills/voiceflow-setup/references/setup.md"
    (site / "setup.md").write_text(rewrite_setup(guide.read_text(), guide, root))
    try:
        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
                                  text=True, timeout=5, check=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True,
                                    text=True, timeout=5, check=True).stdout.strip())
    except (OSError, subprocess.SubprocessError):
        revision, dirty = None, True
    content = {p.relative_to(site).as_posix(): sha(p.read_bytes())
               for p in sorted(site.rglob("*")) if p.is_file()}
    manifest = {
        "schema": 1, "version": json.loads((root / "voiceflow/plugin.json").read_text())["version"],
        "sourceCommit": revision, "hasUncommittedChanges": dirty,
        "contentSHA256": sha(json.dumps(content, sort_keys=True).encode()),
        "files": content,
    }
    (site / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    (output / "SHA256SUMS").write_text("".join(
        f"{sha(p.read_bytes())}  {p.relative_to(output).as_posix()}\n"
        for p in sorted(site.rglob("*")) if p.is_file()))
    return site


if __name__ == "__main__":
    from validate import validate
    validate()
    print(build())
