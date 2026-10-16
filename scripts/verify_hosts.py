"""Verify native plugin discovery in disposable host configurations."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(command, env, cwd):
    result = subprocess.run(command, env=env, cwd=cwd, capture_output=True, text=True, encoding="utf-8", timeout=60)
    if result.returncode:
        raise RuntimeError(f"{command[:3]} failed: {result.stderr[-1000:]}")
    return result.stdout


def main():
    with tempfile.TemporaryDirectory(prefix="voiceflow-hosts-") as temporary:
        directory = Path(temporary)
        for host in ("codex", "claude"):
            if not shutil.which(host):
                print(f"{host}: unavailable; native verification not run")
                continue
            config = directory / host
            config.mkdir()
            key = "CODEX_HOME" if host == "codex" else "CLAUDE_CONFIG_DIR"
            env = dict(os.environ, **{key: str(config)})
            run([host, "plugin", "marketplace", "add", str(ROOT)], env, directory)
            operation = "add" if host == "codex" else "install"
            run([host, "plugin", operation, "voiceflow@voiceflow-plugins"], env, directory)
            inventory = json.loads(run([host, "plugin", "list", "--json"], env, directory))
            entries = inventory["installed"] if host == "codex" else inventory
            assert any(e.get("pluginId", e.get("id")) == "voiceflow@voiceflow-plugins" for e in entries)
            cached = list((config / "plugins/cache").glob("voiceflow-plugins/voiceflow/*/skills"))
            assert len(cached) == 1
            assert len(list(cached[0].glob("*/SKILL.md"))) == 15
            assert (cached[0] / "voiceflow-setup/references/setup.md").is_file()
            print(f"{host}: installed, enabled, and all 15 skills present in isolated cache")
    print("Cursor runtime discovery must be tested in Cursor; no global configuration was changed.")


if __name__ == "__main__":
    main()
