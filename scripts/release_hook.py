"""Optional Codex Stop adapter. Advisory only, gated by explicit environment opt-in."""
import json
import os
import subprocess
import sys
from pathlib import Path


def evaluate(event, enabled, project, run=subprocess.run):
    if not enabled or not project or event.get("stop_hook_active"):
        return {}
    result = run([sys.executable, str(Path(__file__).with_name("harness.py")), "--project", project, "gate"], capture_output=True, text=True, timeout=30, check=False)
    if result.returncode:
        return {"decision": "block", "reason": "Release gate blocked. Report the missing evidence to the artist and stop; do not bypass, retry paid jobs, or approve on their behalf."}
    return {}


if __name__ == "__main__":
    try:
        print(json.dumps(evaluate(json.load(sys.stdin), os.environ.get("OMOTION_RELEASE_HOOK") == "1", os.environ.get("OMOTION_PROJECT"))))
    except (OSError, ValueError, subprocess.SubprocessError):
        print(json.dumps({"systemMessage": "Release hook could not verify the project; use the explicit gate. NOT_RUN."}))
