"""Scan locally with Gitleaks; print locations only, never matched content."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def scan(target, mode, config, executable="gitleaks"):
    with tempfile.TemporaryDirectory(prefix="voiceflow-secret-scan-") as temporary:
        report = Path(temporary) / "report.json"
        command = [executable, mode, str(target), "--config", str(config),
                   "--redact=100", "--no-banner", "--no-color",
                   "--ignore-gitleaks-allow", "--gitleaks-ignore-path", temporary,
                   "--max-decode-depth", "5", "--max-archive-depth", "3",
                   "--timeout", "180", "--exit-code", "10",
                   "--report-format", "json", "--report-path", str(report)]
        if mode == "git":
            command += ["--log-opts=--all --full-history -m"]
        env = {key: value for key, value in os.environ.items()
               if not key.startswith("GITLEAKS_")}
        result = subprocess.run(command, env=env, capture_output=True, text=True,
                                encoding="utf-8", timeout=200)
        if result.returncode not in (0, 10) or not report.is_file():
            # Tool errors can contain source text. Never echo captured output.
            raise RuntimeError(f"Gitleaks {mode} scan failed (exit {result.returncode}); no pass recorded")
        findings = json.loads(report.read_text(encoding="utf-8")) or []
        if bool(findings) != (result.returncode == 10):
            raise RuntimeError("Gitleaks exit code and findings disagree")
        return [{key: finding.get(key) for key in ("RuleID", "File", "StartLine", "Commit")}
                for finding in findings]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gitleaks", default="gitleaks", help="Path to the Gitleaks executable")
    args = parser.parse_args()
    try:
        shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT,
                                 capture_output=True, text=True, timeout=10, check=True)
        if shallow.stdout.strip() != "false":
            raise RuntimeError("Full Git history is required; fetch unshallow before scanning")
        if not (ROOT / "dist/site/agents/voiceflow.zip").is_file():
            raise RuntimeError("Build the package before scanning its generated files and archives")
        failed = False
        for label, mode, target in (("Git history (all fetched refs)", "git", ROOT),
                                    ("Working files", "dir", ROOT),
                                    ("Generated packages", "dir", ROOT / "dist")):
            findings = scan(target, mode, ROOT / ".gitleaks.toml", args.gitleaks)
            print(f"{label}: {len(findings)} findings")
            for finding in findings:
                print(json.dumps(finding, ensure_ascii=True))
            failed |= bool(findings)
        return 1 if failed else 0
    except (OSError, subprocess.SubprocessError, ValueError, RuntimeError) as error:
        # Do not print exceptions containing subprocess args/output or source text.
        print(str(error) if isinstance(error, RuntimeError) else
              "Secret scan could not complete; check Gitleaks installation and repository state")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
