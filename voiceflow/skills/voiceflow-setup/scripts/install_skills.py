"""Install portable skills without replacing user edits. Python 3.10+."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

RECEIPT = ".voiceflow-skills.json"
SOURCE = Path(__file__).resolve().parents[2]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(source):
    result = {}
    for path in sorted(source.rglob("*")):
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            raise ValueError("Skill sources must not contain symlinks")
        if path.is_file():
            result[path.relative_to(source).as_posix()] = path.read_bytes()
    if "voiceflow/SKILL.md" not in result:
        raise ValueError("The complete Voiceflow skill tree is required")
    return result


def safe_path(target, relative):
    parts = relative.split("/")
    if (not parts or parts[0] != "voiceflow" and not parts[0].startswith("voiceflow-")
            or any(part in ("", ".", "..") or "\\" in part or ":" in part for part in parts)):
        raise ValueError("Invalid managed skill path")
    current = target
    for part in parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"Symlink destination refused: {relative}")
    return current


def apply_changes(target, changes):
    """Preflight happens before this; backups allow rollback on partial I/O failure."""
    originals = {path: path.read_bytes() if path.exists() else None for path in changes}
    completed = []
    target.mkdir(parents=True, exist_ok=True)
    try:
        for path, data in changes.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            if data is None:
                path.unlink(missing_ok=True)
            else:
                handle, name = tempfile.mkstemp(prefix=".voiceflow-", dir=path.parent)
                try:
                    with os.fdopen(handle, "wb") as stream:
                        stream.write(data)
                    os.replace(name, path)
                finally:
                    Path(name).unlink(missing_ok=True)
            completed.append(path)
    except OSError:
        for path in reversed(completed):
            original = originals[path]
            if original is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(original)
        raise


def install(source, target, update=False, uninstall=False):
    target = target.expanduser().resolve()
    receipt = target / RECEIPT
    if receipt.is_symlink():
        raise ValueError("Symlink receipt refused")
    previous = json.loads(receipt.read_text(encoding="utf-8")) if receipt.exists() else {"files": {}}
    if not isinstance(previous.get("files"), dict):
        raise ValueError("Invalid installation receipt")
    old = previous["files"]
    for relative, expected in old.items():
        path = safe_path(target, relative)
        if not path.is_file() or digest(path.read_bytes()) != expected:
            raise ValueError(f"Local change preserved: {relative}")
    if uninstall:
        if not receipt.exists():
            return "not_installed"
        changes = {safe_path(target, name): None for name in old}
        changes[receipt] = None
        apply_changes(target, changes)
        return "removed"

    incoming = inventory(source)
    hashes = {name: digest(data) for name, data in incoming.items()}
    if old and hashes != old and not update:
        raise ValueError("A different version is installed; use --update intentionally")
    changes = {}
    for name, data in incoming.items():
        path = safe_path(target, name)
        if path.exists() and not path.is_file():
            raise ValueError(f"Destination is not a file: {name}")
        if path.exists() and path.read_bytes() != data and name not in old:
            raise ValueError(f"Existing file preserved: {name}")
        if not path.exists() or path.read_bytes() != data:
            changes[path] = data
    for name in old.keys() - incoming.keys():
        changes[safe_path(target, name)] = None
    if not changes and old == hashes:
        return "unchanged"
    changes[receipt] = (json.dumps({"schema": 1, "files": hashes}, sort_keys=True, indent=2) + "\n").encode()
    apply_changes(target, changes)
    return "installed"


def client_target(client):
    if client == "codex":
        return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills"
    if client == "claude":
        return Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude"))) / "skills"
    return Path.home() / ".cursor" / "skills"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", choices=("claude", "codex", "cursor"), required=True)
    parser.add_argument("--target", type=Path)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--update", action="store_true")
    action.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()
    target = args.target or client_target(args.client)
    try:
        status = install(SOURCE, target, args.update, args.uninstall)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\nNo conflicting file was overwritten.\n")
    print(json.dumps({"status": status, "target": str(target.expanduser().resolve())}))


if __name__ == "__main__":
    main()
