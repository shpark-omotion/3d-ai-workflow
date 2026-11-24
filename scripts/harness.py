#!/usr/bin/env python3
"""Local cooperative production gate. No provider calls, installs or credentials."""
import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import uuid
from contextlib import contextmanager
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
CHECKER = KIT / "scripts/blender/qa.py"
CHECKS = ("mesh", "topology", "uv", "material", "textures", "rig", "shapes", "protected")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def json_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    fd, name = tempfile.mkstemp(dir=path.parent, prefix=".state-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def workspace(path):
    p = Path(path).absolute()
    require(p.resolve() == p and not any(x.is_symlink() for x in (p, *p.parents)), "Use a real, non-linked project path")
    require(p != KIT and KIT not in p.parents and p not in KIT.parents, "Project must be outside the kit")
    return p


def inside(root, relative):
    rel = Path(relative)
    require(not rel.is_absolute() and ".." not in rel.parts, "Unsafe relative path")
    p = root / rel
    require(p.resolve() == p and root in p.parents and not any(x.is_symlink() for x in (p, *p.parents)), "Linked/escaping path")
    return p


@contextmanager
def locked(root):
    lock = inside(root, ".writer-lock")
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(fd, "w") as f:
            f.write(str(os.getpid()))
        yield
    finally:
        lock.unlink()


def policy_ok(p):
    require(isinstance(p, dict) and isinstance(p.get("target"), str) and p["target"].strip(), "Set target")
    require(type(p.get("max_triangles")) is int and p["max_triangles"] > 0, "Set positive triangle budget")
    for k in ("max_credits", "max_attempts"):
        require(type(p.get(k)) is int and p[k] >= 0, "Set nonnegative integer " + k)
    for k in ("require_uv", "require_material", "require_rig", "require_motion", "require_runtime"):
        require(type(p.get(k)) is bool, "Set boolean " + k)
    for k in ("open_meshes", "required_bones", "required_shapes"):
        require(isinstance(p.get(k), list) and all(isinstance(x, str) and x for x in p[k]), "Set names list " + k)
    frames = p.get("motion_frames", [])
    require(isinstance(frames, list) and len(frames) <= 12 and all(type(x) is int and x >= 0 for x in frames), "Set up to 12 nonnegative motion frames")
    require(not p["require_motion"] or len(set(frames)) >= 2, "Motion requires two distinct sample frames")
    require(not p["required_bones"] or p["require_rig"], "Bone rules require rig")
    require(not p["require_motion"] or p["require_rig"], "Motion requires rig")
    require(p["target"] == "Blender test" or p["require_runtime"], "Non-test target requires runtime review")
    require(not p.get("face_mesh") or isinstance(p["face_mesh"], str), "Set face_mesh name")
    require(p.get("front") in ("-Y", "+Y", "-X", "+X"), "Set front axis")


def check_glb(path):
    """Container framing and no external URIs; not full glTF conformance."""
    require(path.suffix.lower() == ".glb", "v0.2 accepts self-contained GLB only")
    with path.open("rb") as f:
        header = f.read(12)
        require(len(header) == 12, "Truncated GLB")
        magic, version, size = struct.unpack("<4sII", header)
        require(magic == b"glTF" and version == 2 and size == path.stat().st_size, "Invalid GLB header")
        chunk = f.read(8)
        require(len(chunk) == 8, "Missing JSON chunk")
        n, typ = struct.unpack("<I4s", chunk)
        require(typ == b"JSON" and n % 4 == 0 and 0 < n <= min(size - 20, 32 * 1024 * 1024), "Invalid JSON chunk")
        obj = json.loads(f.read(n).decode("utf-8"))
        require(obj.get("asset", {}).get("version") == "2.0", "Not glTF 2.0")
        for key in ("buffers", "images"):
            for item in obj.get(key, []):
                require("uri" not in item or (isinstance(item["uri"], str) and item["uri"].startswith("data:")), "External URI not accepted")
        while f.tell() < size:
            chunk = f.read(8)
            require(len(chunk) == 8, "Truncated chunk")
            n, typ = struct.unpack("<I4s", chunk)
            require(n % 4 == 0 and f.tell() + n <= size, "Invalid chunk size")
            f.seek(n, 1)
    return digest(path)


def current(root, s):
    require(s.get("candidate"), "No candidate")
    p = inside(root, s["candidate"]["path"])
    require(p.is_file() and digest(p) == s["candidate"]["sha"], "Candidate changed; register a new version")
    return p


def evidence(root, s, require_pass=True):
    current(root, s)
    qa = s.get("qa")
    require(isinstance(qa, dict), "QA NOT_RUN")
    report = inside(root, qa["report"])
    require(digest(report) == qa["sha"], "QA evidence changed")
    q = read(report)
    require(q.get("schema") == 1 and q.get("asset_sha") == s["candidate"]["sha"] and q.get("policy_sha") == json_hash(s["policy"]) and q.get("checker_sha") == digest(CHECKER) and q.get("protected_sha") == json_hash(s["candidate"]["protected"]), "Stale QA")
    require(set(q.get("checks", {})) == set(CHECKS), "Required checks missing")
    if require_pass:
        require(all(v.get("status") == "PASS" for v in q["checks"].values()), "Required technical QA failed or missing")
    views = {"front.png", "left.png", "back.png", "right.png"}
    if s["policy"].get("face_mesh"):
        views.add("face.png")
    views.update("pose_" + str(f) + ".png" for f in s["policy"].get("motion_frames", []))
    require(set(q.get("renders", {})) == views, "Required views missing")
    for name, sha in q["renders"].items():
        require(digest(inside(root, str(Path(qa["report"]).parent / name))) == sha, "Render changed")
    return q


def release_gate(root, s):
    evidence(root, s)
    for ref in s["references"]:
        require(digest(inside(root, ref["path"])) == ref["sha"], "Reference changed")
    required = ["design", "appearance"] + (["expression"] if s["policy"]["required_shapes"] else []) + (["motion"] if s["policy"]["require_motion"] else []) + (["runtime"] if s["policy"]["require_runtime"] else [])
    for k in required:
        ap = s["approvals"].get(k, {})
        require(ap.get("asset") == s["candidate"]["sha"] and ap.get("qa") == s["qa"]["sha"] and ap.get("actor"), "Missing approval: " + k)
    require(not any(x["status"] in ("RESERVED", "UNKNOWN") for x in s["attempts"]), "Unresolved generation")
    require(sum(max(x["reserved"], x.get("actual", 0)) for x in s["attempts"]) <= s["policy"]["max_credits"], "Credit overrun requires owner review")


def mutate(root, s, a):
    cmd = a.command
    if cmd == "reference":
        source = Path(a.file).resolve(strict=True)
        require(source.is_file() and source.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp") and a.note.strip(), "Image and design note required")
        rel = "references/" + uuid.uuid4().hex + source.suffix.lower()
        dst = inside(root, rel)
        dst.parent.mkdir(exist_ok=True)
        with dst.open("xb") as f, source.open("rb") as src:
            shutil.copyfileobj(src, f)
        s["references"].append({"path": rel, "sha": digest(dst), "view": a.view, "note": a.note})
        s["approvals"] = {}
    elif cmd == "snapshot":
        source = Path(a.file).resolve(strict=True)
        check_glb(source)
        previous = s.get("candidate") or {}
        baseline = dict(previous.get("protected", {}))
        frame = previous.get("frame")
        if a.protect:
            q = evidence(root, s, require_pass=False)
            for name in a.protect:
                require(name in q["objects"], "Unknown protected object: " + name)
                baseline.setdefault(name, q["objects"][name])
            frame = frame or q.get("frame")
        rel = "versions/" + uuid.uuid4().hex + "/candidate.glb"
        dst = inside(root, rel)
        dst.parent.mkdir(parents=True, exist_ok=False)
        shutil.copyfile(source, dst)
        sha = check_glb(dst)
        if a.attempt:
            require(any(x["id"] == a.attempt and x["status"] == "SUCCESS" for x in s["attempts"]), "Attempt must be reconciled SUCCESS")
        item = {"path": rel, "sha": sha, "protected": baseline, "frame": frame, "provider_attempt": a.attempt or previous.get("provider_attempt")}
        s["versions"].append(item)
        s.update(candidate=item, qa=None, approvals={})
    elif cmd == "move-static":
        from static_offset import move
        old = current(root, s)
        require(a.actor.strip() and a.note.strip(), "Explicit human-approved edit scope required")
        require(a.node not in s["candidate"]["protected"], "Protected mesh")
        rel = "versions/" + uuid.uuid4().hex + "/candidate.glb"
        dst = inside(root, rel); dst.parent.mkdir(parents=True, exist_ok=False)
        change = move(old, dst, a.node, a.delta)
        baseline = dict(s["candidate"]["protected"]); frame = s["candidate"].get("frame")
        if s.get("qa"):
            q = evidence(root, s, require_pass=False)
            for name, sig in q["objects"].items():
                if name != a.node:
                    baseline.setdefault(name, sig)
            frame = frame or q.get("frame")
        item = dict(s["candidate"], path=rel, sha=digest(dst), protected=baseline, frame=frame, edit={**change, "actor": a.actor, "note": a.note})
        s["versions"].append(item); s.update(candidate=item, qa=None, approvals={})
    elif cmd == "reserve":
        require(a.credits > 0 and a.actor.strip() and a.request.strip(), "Positive credits, exact generation request and human approval required")
        attempts = s["attempts"]
        require(not any(x["status"] in ("RESERVED", "UNKNOWN") for x in attempts), "Reconcile previous attempt first")
        require(len(attempts) < s["policy"]["max_attempts"], "Attempt limit")
        require(sum(max(x["reserved"], x.get("actual", 0)) for x in attempts) + a.credits <= s["policy"]["max_credits"], "Credit limit")
        attempts.append({"id": uuid.uuid4().hex, "route": a.route, "reserved": a.credits, "actor": a.actor, "request": a.request, "references": [x["sha"] for x in s["references"]], "status": "RESERVED"})
    elif cmd == "reconcile":
        hits = [x for x in s["attempts"] if x["id"] == a.id]
        require(len(hits) == 1 and hits[0]["status"] in ("RESERVED", "UNKNOWN"), "No unresolved attempt")
        require(a.note.strip() and (a.status == "UNKNOWN" or (a.actual is not None and a.actual >= 0)), "Record verified cost and observation")
        require(a.status != "SUCCESS" or bool(a.task_id.strip()), "Record provider task ID or Studio result ID")
        require(a.actual is None or a.actual >= 0, "Cost cannot be negative")
        hits[0].update(status=a.status, actual=max(hits[0].get("actual", 0), a.actual or 0), task_id=a.task_id or hits[0].get("task_id", ""), note=a.note)
    elif cmd == "qa":
        asset = current(root, s)
        exe = Path(a.blender).resolve(strict=True)
        require(exe.is_file(), "Select approved Blender executable")
        s.update(qa=None, approvals={})
        write(inside(root, "state.json"), s)
        rel = "qa/" + uuid.uuid4().hex
        folder = inside(root, rel)
        folder.mkdir(parents=True, exist_ok=False)
        request = {"asset_sha": s["candidate"]["sha"], "policy": s["policy"], "policy_sha": json_hash(s["policy"]), "checker_sha": digest(CHECKER), "protected": s["candidate"]["protected"], "protected_sha": json_hash(s["candidate"]["protected"]), "frame": s["candidate"].get("frame")}
        write(folder / "request.json", request)
        with (folder / "blender.log").open("wb") as log:
            result = subprocess.run([str(exe), "--background", "--factory-startup", "--disable-autoexec", "--python-exit-code", "3", "--python", str(CHECKER), "--", str(asset), str(folder)], stdout=log, stderr=subprocess.STDOUT, timeout=600, check=False)
        require(result.returncode == 0 and (folder / "report.json").is_file(), "Blender QA incomplete; inspect " + rel)
        current(root, s)
        s["qa"] = {"report": rel + "/report.json", "sha": digest(folder / "report.json")}
        try:
            q = evidence(root, s)
            s["qa"].update(status="PASS", checks=q["checks"])
        except (ValueError, OSError, KeyError, TypeError) as e:
            s["qa"].update(status="FAIL", reason=str(e))
    elif cmd == "approve":
        evidence(root, s)
        require(a.actor.strip() and a.note.strip(), "Human identity and observation required")
        s["approvals"][a.kind] = {"actor": a.actor, "note": a.note, "asset": s["candidate"]["sha"], "qa": s["qa"]["sha"]}
    elif cmd == "deliver":
        release_gate(root, s)
        dst = inside(root, "delivery/" + uuid.uuid4().hex + "/character.glb")
        dst.parent.mkdir(parents=True, exist_ok=False)
        shutil.copyfile(current(root, s), dst)
        require(digest(dst) == s["candidate"]["sha"], "Delivery hash mismatch")
        s["deliveries"].append({"path": str(dst.relative_to(root)), "sha": digest(dst), "qa": s["qa"], "approvals": dict(s["approvals"])})
    else:
        raise ValueError("Unknown command")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init"); init.add_argument("--policy", required=True)
    sub.add_parser("status")
    sub.add_parser("gate")
    ref = sub.add_parser("reference"); ref.add_argument("file"); ref.add_argument("--view", choices=["front", "left", "back", "right", "face", "other"], required=True); ref.add_argument("--note", required=True)
    snap = sub.add_parser("snapshot"); snap.add_argument("file"); snap.add_argument("--protect", action="append", default=[]); snap.add_argument("--attempt")
    m = sub.add_parser("move-static"); m.add_argument("node"); m.add_argument("--delta", type=float, nargs=3, required=True); m.add_argument("--actor", required=True); m.add_argument("--note", required=True)
    r = sub.add_parser("reserve"); r.add_argument("--route", choices=["studio", "plugin", "comfyui"], required=True); r.add_argument("--credits", type=int, required=True); r.add_argument("--actor", required=True); r.add_argument("--request", required=True)
    r = sub.add_parser("reconcile"); r.add_argument("id"); r.add_argument("--status", choices=["SUCCESS", "FAILED", "UNKNOWN"], required=True); r.add_argument("--actual", type=int); r.add_argument("--task-id", default=""); r.add_argument("--note", required=True)
    qa = sub.add_parser("qa"); qa.add_argument("--blender", required=True)
    ap = sub.add_parser("approve"); ap.add_argument("kind", choices=["design", "appearance", "expression", "motion", "runtime"]); ap.add_argument("--actor", required=True); ap.add_argument("--note", required=True)
    sub.add_parser("deliver")
    a = parser.parse_args(argv)
    try:
        root = workspace(a.project)
        state = inside(root, "state.json")
        if a.command == "init":
            p = read(Path(a.policy)); policy_ok(p)
            root.mkdir(parents=True, exist_ok=False)
            write(state, {"schema": 1, "id": uuid.uuid4().hex, "policy": p, "candidate": None, "versions": [], "references": [], "attempts": [], "qa": None, "approvals": {}, "deliveries": []})
        elif a.command == "gate":
            with locked(root):
                s = read(state); policy_ok(s["policy"]); release_gate(root, s)
        elif a.command != "status":
            with locked(root):
                s = read(state); require(s.get("schema") == 1, "Unsupported state"); policy_ok(s["policy"])
                mutate(root, s, a)
                write(state, s)
        result = read(state)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if a.command == "qa" and result["qa"]["status"] != "PASS" else 0
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError, KeyError, TypeError, AttributeError) as e:
        print("BLOCKED:", e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
