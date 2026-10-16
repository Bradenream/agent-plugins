"""Verify the released CLI contract using only help and a local fixture server."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import importlib.util
import json
from pathlib import Path
import subprocess
import threading

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vf", required=True)
    args = parser.parse_args()
    module_path = ROOT / "voiceflow/skills/voiceflow-setup/scripts/check_connection.py"
    spec = importlib.util.spec_from_file_location("probe", module_path)
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)
    for command in (["version"], ["auth", "login", "--help"], ["workspace", "list", "--help"],
                    ["docs", "search", "--help"], ["docs", "get", "--help"],
                    ["workflow", "insert-step", "--help"], ["agent", "patch-prompt", "--help"]):
        result = subprocess.run([args.vf, *command], capture_output=True, text=True, encoding="utf-8", timeout=10, check=True)
        if command[:2] == ["auth", "login"]:
            assert all(flag in result.stdout for flag in ("--no-browser", "--login-timeout"))
    requested = []
    scenario = {"status": 200, "body": {"workspaces": []}}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            requested.append(self.path)
            self.send_response(scenario["status"])
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(scenario["body"]).encode())

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        for status, expected in ((200, "connected"), (401, "authentication_required"),
                                 (403, "permission_denied"), (429, "temporarily_unavailable"),
                                 (503, "temporarily_unavailable")):
            scenario.update(status=status, body={"workspaces": []} if status == 200 else {"message": "fixture failure"})
            result = subprocess.run([
                args.vf, "workspace", "list", "--agent-mode", "--no-interactive", "--timeout", "2s",
                "-o", "json", "--server-url", f"http://127.0.0.1:{server.server_port}",
                "--token", "local-fixture-not-a-credential",
            ], capture_output=True, text=True, encoding="utf-8", timeout=20)
            actual = probe.classify(result.returncode, result.stdout, result.stderr)
            assert actual == expected, (status, actual, result.returncode, result.stdout, result.stderr, requested)
        assert requested and all(path == "/v1/stable/workspace" for path in requested)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    print("CLI help and five local HTTP scenarios passed; no Voiceflow account was contacted.")


if __name__ == "__main__":
    main()
