"""Reject releases outside the protected default branch; read-only GitHub access."""
import argparse
import json
import re
import subprocess
from urllib.parse import quote


def github_json(endpoint):
    result = subprocess.run(["gh", "api", endpoint], capture_output=True, text=True,
                            encoding="utf-8", timeout=30)
    if result.returncode:
        raise RuntimeError("Could not verify release source with GitHub; release blocked")
    return json.loads(result.stdout)


def verify(repository, commit, version, workflow_ref, api=github_json):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Use an owner/repository identifier")
    if not re.fullmatch(r"[a-f0-9]{40}", commit):
        raise ValueError("Use a full source commit SHA")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Use a package version without v")
    prefix = "repos/" + repository
    default = api(prefix)["default_branch"]
    if not default or workflow_ref != "refs/heads/" + default:
        raise ValueError("Run the release workflow from the default branch")
    branch = api(prefix + "/branches/" + quote(default, safe=""))
    if branch.get("protected") is not True:
        raise ValueError("Releases require a protected default branch")
    head = branch["commit"]["sha"]
    if not re.fullmatch(r"[a-f0-9]{40}", head):
        raise ValueError("Invalid default branch revision")
    # Compare against the just-read immutable head, not a moving branch name.
    comparison = api(prefix + "/compare/" + commit + "..." + head)
    if (comparison.get("status") not in ("identical", "ahead")
            or comparison.get("merge_base_commit", {}).get("sha") != commit):
        raise ValueError("Release commit must already be on the default branch")
    return default


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repository", "commit", "version", "workflow-ref"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    try:
        branch = verify(args.repository, args.commit, args.version, args.workflow_ref)
        print(f"Release source verified on protected branch {branch}")
        return 0
    except (ValueError, RuntimeError) as error:
        print(str(error) if not isinstance(error, json.JSONDecodeError) else
              "Invalid GitHub response; release blocked")
    except (OSError, subprocess.SubprocessError, KeyError, TypeError):
        print("Release source verification could not complete; release blocked")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
