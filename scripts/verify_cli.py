"""Verify the released CLI contract using only help and a local fixture server."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import importlib.util
import json
from pathlib import Path
import subprocess
import threading
import time
from urllib.parse import parse_qs, urlsplit

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
                    ["workflow", "insert-step", "--help"], ["agent", "patch-prompt", "--help"],
                    ["widget", "get", "--help"], ["widget", "get-snippet", "--help"],
                    ["widget", "update", "--help"]):
        result = subprocess.run([args.vf, *command], capture_output=True, text=True, encoding="utf-8", timeout=10, check=True)
        if command[:2] == ["auth", "login"]:
            assert all(flag in result.stdout for flag in ("--no-browser", "--login-timeout"))
    requested = []
    scenario = {"status": 200, "body": {"workspaces": []}}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            requested.append(("GET", self.path, None))
            self.respond()

        def do_PATCH(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            requested.append(("PATCH", self.path, body))
            self.respond()

        def respond(self):
            body = scenario.get("raw", json.dumps(scenario["body"]).encode())
            self.send_response(scenario["status"])
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            # A split response exercises the released CLI's early-cancel edge case.
            self.wfile.flush()
            time.sleep(0.05)
            self.wfile.write(body)

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
                args.vf, "workspace", "list", "--agent-mode", "--no-interactive",
                "-o", "json", "--color", "never", "--server-url", f"http://127.0.0.1:{server.server_port}",
                "--token", "local-fixture-not-a-credential",
            ], capture_output=True, text=True, encoding="utf-8", timeout=20)
            actual = probe.classify(result.returncode, result.stdout, result.stderr)
            assert actual == expected, (status, actual, result.returncode, result.stdout, result.stderr, requested)
        for body in (b'', b'{"workspaces":[', b'{"workspaces":[]} trailing'):
            scenario.update(status=200, raw=body)
            result = subprocess.run([
                args.vf, "workspace", "list", "--agent-mode", "--no-interactive",
                "-o", "json", "--color", "never", "--server-url", f"http://127.0.0.1:{server.server_port}",
                "--token", "local-fixture-not-a-credential",
            ], capture_output=True, text=True, encoding="utf-8", timeout=20)
            assert probe.classify(result.returncode, result.stdout, result.stderr) != "connected"
        scenario.pop("raw")
        assert requested and all(method == "GET" and path == "/v1/stable/workspace"
                                 for method, path, _ in requested)

        # Exercise the documented widget commands against localhost, never an account.
        patch = {"common": {"primaryColor": {"color": "#245D58"}}}
        query = {"projectID": ["fixture-project"], "environmentAlias": ["preview"]}
        widget_cases = (
            (["get"], None, "GET", "/v1/stable/widget", query,
             {"widget": patch}),
            (["get-snippet"], None, "GET", "/v1/stable/widget/snippet",
             {**query, "version": ["published"]}, {"snippet": "fixture-embed-published"}),
            (["get-snippet", "--version-param", "draft"], None, "GET", "/v1/stable/widget/snippet",
             {**query, "version": ["draft"]}, {"snippet": "fixture-embed-draft"}),
            (["update"], patch, "PATCH", "/v1/stable/widget", query, {"widget": patch}),
        )
        for command, body, method, path, expected_query, response in widget_cases:
            scenario.update(status=200, body=response)
            previous_count = len(requested)
            result = subprocess.run([
                args.vf, "widget", *command, "--project-id", "fixture-project",
                "--environment-alias", "preview", "--timeout", "2s", "-o", "toon",
                "--no-interactive", "--color", "never",
                "--server-url", f"http://127.0.0.1:{server.server_port}",
                "--token", "local-fixture-not-a-credential",
            ], input=json.dumps(body) if body is not None else None,
                capture_output=True, text=True, encoding="utf-8", timeout=20)
            assert result.returncode == 0, (command, result.stdout, result.stderr)
            assert len(requested) == previous_count + 1, (command, requested)
            actual_method, actual_url, actual_body = requested[-1]
            parsed = urlsplit(actual_url)
            assert (actual_method, parsed.path, parse_qs(parsed.query), actual_body) == (
                method, path, expected_query, body), requested[-1]
            assert result.stdout.strip(), (command, "empty success response")
            if "snippet" in response:
                assert response["snippet"] in result.stdout, result.stdout
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    print("CLI help, five connection scenarios, three malformed responses, and four widget contracts passed against localhost; no Voiceflow account was contacted.")


if __name__ == "__main__":
    main()
