#!/usr/bin/env python3
"""Read-only PATH and local-kit check. Never installs or contacts services."""
import argparse
import json
import platform
import shutil
from pathlib import Path


def inspect(root, which=shutil.which):
    """Presence only; no execution of discovered binaries or credential access."""
    binaries = {}
    for name in ("codex", "blender", "uvx", "node", "git"):
        binaries[name] = "FOUND_ON_PATH" if which(name) else "NOT_FOUND_ON_PATH"
    files = {}
    for relative in (
        "README.md", "AGENTS.md", ".gitignore",
        ".agents/skills/character-production/SKILL.md",
        "docs/START-HERE.md", "docs/SETUP.md", "docs/PRODUCTION-GUIDE.md",
        "docs/QUALITY-GUIDE.md", "templates/character-spec.md",
        "templates/run-state.md", "templates/runtime-check.md",
    ):
        files[relative] = "PRESENT" if (root / relative).is_file() else "MISSING"
    return {
        "os": platform.system(),
        "path_checks": binaries,
        "kit_files": files,
        "runtime_checks": {key: "NOT_RUN" for key in (
            "astra_selected", "codex_app", "skill_loaded", "tripo_login", "blender_app",
            "blender_mcp_scene_read", "computer_use", "tripo_plugin", "asset_permissions"
        )},
        "note": "PATH presence is not installation, version compatibility, or connectivity proof. GUI apps may not be on PATH. No remote calls.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Machine-readable report")
    args = parser.parse_args()
    report = inspect(Path(__file__).resolve().parents[1])
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("OS:", report["os"])
        for section in ("path_checks", "kit_files", "runtime_checks"):
            print(f"\n{section}:")
            for name, status in report[section].items():
                print(f"  {name}: {status}")
        print("\n" + report["note"])
    return 1 if "MISSING" in report["kit_files"].values() else 0


if __name__ == "__main__":
    raise SystemExit(main())
