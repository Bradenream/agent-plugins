"""Read-only connection probe. Never echo service output or credentials."""
import argparse
import json
import re
import subprocess


def classify(returncode, stdout, stderr):
    payloads = []
    for stream in (stdout, stderr):
        try:
            payloads.append(json.loads(stream))
        except (ValueError, TypeError):
            pass
    for payload in payloads:
        if not isinstance(payload, dict):
            continue
        kind = payload.get("error_type")
        if kind == "authentication_error":
            return "authentication_required"
        if kind == "authorization_error":
            return "permission_denied"
        if kind in ("connection_error", "rate_limit_error", "server_error"):
            return "temporarily_unavailable"
        if kind or payload.get("error"):
            return "request_failed"
    if returncode == 0:
        for payload in payloads[:1]:
            if isinstance(payload, dict) and isinstance(payload.get("workspaces"), list):
                return "connected"
        # Only the typed workspace-list envelope is accepted, not arbitrary text.
        if re.match(r"\Aworkspaces\[\d+\](?:\{[^{}\r\n]+\})?:[ \t]*(?:\r?\n|\Z)", stdout):
            return "connected"
    return "unexpected_response"


def check(binary, timeout=25):
    try:
        result = subprocess.run(
            [binary, "workspace", "list", "--agent-mode", "--no-interactive",
             "--timeout", "20s", "--color", "never", "-o", "toon"],
            capture_output=True, text=True, encoding="utf-8", timeout=timeout, check=False,
        )
    except FileNotFoundError:
        return "cli_missing"
    except subprocess.TimeoutExpired:
        return "temporarily_unavailable"
    except OSError:
        return "cli_unavailable"
    return classify(result.returncode, result.stdout, result.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vf", default="vf", help="Path to the verified Voiceflow CLI")
    args = parser.parse_args()
    status = check(args.vf)
    print(json.dumps({"status": status}))
    return 0 if status == "connected" else 1


if __name__ == "__main__":
    raise SystemExit(main())
