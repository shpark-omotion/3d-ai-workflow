"""Local CLI and gate tests. Fake Blender reports test orchestration, not 3D QA."""
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

KIT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KIT / "scripts"), str(KIT / "examples")]
import harness as h
from make_fixture import build


class HarnessTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / "project"
        self.policy = dict(h.read(KIT / "examples/policy.json"), max_credits=10, max_attempts=2)
        self.policy_path = self.root / "policy.json"
        self.policy_path.write_text(json.dumps(self.policy))
        self.assertEqual(self.cli("init", "--policy", self.policy_path), 0)
        self.original = self.root / "base.glb"
        build(self.original)

    def cli(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return h.main(["--project", str(self.project), *map(str, args)])

    def state(self):
        return h.read(self.project / "state.json")

    def snapshot(self, file=None, *args):
        return self.cli("snapshot", file or self.original, *args)

    def fake(self, status="PASS", objects=None):
        def run(cmd, **kw):
            folder = Path(cmd[-1]); req = h.read(folder / "request.json")
            renders = {}
            for name in ("front", "left", "back", "right", "face"):
                p = folder / (name + ".png"); p.write_bytes(b"mock view")
                renders[p.name] = h.digest(p)
            checks = {k: {"status": status, "findings": []} for k in h.CHECKS}
            h.write(folder / "report.json", {"schema": 1, **{k: req[k] for k in ("asset_sha", "policy_sha", "checker_sha", "protected_sha")}, "checks": checks, "renders": renders, "objects": objects or {"Head": "head-original"}, "frame": {"center": [0,0,0], "span": 3}})
            return subprocess.CompletedProcess(cmd, 0)
        with patch.object(h.subprocess, "run", side_effect=run):
            return self.cli("qa", "--blender", sys.executable)

    def approve(self, kind):
        return self.cli("approve", kind, "--actor", "test-human", "--note", "synthetic check")

    def test_glb_snapshot_original_preserved(self):
        original = h.digest(self.original)
        self.assertEqual(self.snapshot(), 0)
        self.assertEqual(h.digest(self.original), original)
        self.assertEqual(self.state()["candidate"]["sha"], original)
        self.assertNotEqual(self.cli("init", "--policy", self.policy_path), 0)

    def test_invalid_and_external_glb(self):
        other = self.root / "external.glb"; build(other, external=True)
        self.assertNotEqual(self.snapshot(other), 0)
        broken = self.root / "broken.glb"; broken.write_bytes(b"bad")
        self.assertNotEqual(self.snapshot(broken), 0)

    def test_unresolved_attempt_and_budget(self):
        self.assertEqual(self.cli("reserve", "--route", "studio", "--credits", 6, "--actor", "human", "--request", "P2 fixture"), 0)
        attempt = self.state()["attempts"][0]["id"]
        self.assertEqual(self.cli("reconcile", attempt, "--status", "UNKNOWN", "--note", "timeout"), 0)
        self.assertNotEqual(self.cli("reserve", "--route", "plugin", "--credits", 1, "--actor", "human", "--request", "P2 fixture"), 0)
        self.assertEqual(self.cli("reconcile", attempt, "--status", "FAILED", "--actual", 6, "--note", "verified history"), 0)
        self.assertNotEqual(self.cli("reserve", "--route", "studio", "--credits", 5, "--actor", "human", "--request", "P2 fixture"), 0)
        self.assertEqual(self.cli("reserve", "--route", "studio", "--credits", 4, "--actor", "human", "--request", "P2 fixture"), 0)

    def test_missing_failed_and_stale_qa_block(self):
        self.assertEqual(self.snapshot(), 0)
        self.assertNotEqual(self.cli("deliver"), 0)
        self.assertEqual(self.fake("FAIL"), 2)
        self.assertNotEqual(self.approve("design"), 0)
        self.assertEqual(self.fake(), 0)
        self.assertEqual(self.approve("design"), 0)
        self.assertNotEqual(self.cli("deliver"), 0)
        self.assertEqual(self.approve("appearance"), 0)
        self.assertEqual(self.cli("gate"), 0)
        self.assertEqual(self.cli("deliver"), 0)
        candidate = self.project / self.state()["candidate"]["path"]
        candidate.write_bytes(b"changed")
        self.assertNotEqual(self.cli("deliver"), 0)

    def test_repair_keeps_baseline_even_after_failed_qa(self):
        self.assertEqual(self.snapshot(), 0)
        self.assertEqual(self.fake("FAIL"), 2)
        repaired = self.root / "repair.glb"; build(repaired, hair_offset=0.2)
        self.assertEqual(self.snapshot(repaired, "--protect", "Head"), 0)
        s = self.state(); self.assertEqual(s["candidate"]["protected"], {"Head": "head-original"})
        self.assertIsNone(s["qa"])
        self.assertEqual(self.snapshot(self.original), 0)
        self.assertEqual(self.state()["candidate"]["protected"], {"Head": "head-original"})
        self.assertNotEqual(self.cli("deliver"), 0)

    def test_lock_and_symlink(self):
        with h.locked(self.project):
            self.assertNotEqual(self.snapshot(), 0)
        link = self.project / "versions"
        try:
            link.symlink_to(self.root, target_is_directory=True)
        except OSError:
            self.skipTest("symlinks unavailable")
        self.assertNotEqual(self.snapshot(), 0)

    def test_render_and_reference_tamper(self):
        self.assertEqual(self.snapshot(), 0)
        self.assertEqual(self.fake(), 0)
        self.assertEqual(self.approve("design"), 0)
        self.assertEqual(self.approve("appearance"), 0)
        report = self.project / self.state()["qa"]["report"]
        (report.parent / "front.png").write_bytes(b"tampered")
        self.assertNotEqual(self.cli("deliver"), 0)
        img = self.root / "reference.png"; img.write_bytes(b"synthetic bytes")
        self.assertEqual(self.cli("reference", img, "--view", "front", "--note", "test"), 0)
        self.assertEqual(self.state()["approvals"], {})

    def test_real_static_local_repair(self):
        import struct
        def chunks(path):
            b = path.read_bytes(); n = struct.unpack_from("<I", b, 12)[0]
            return json.loads(b[20:20+n]), b[20+n:]
        self.assertEqual(self.snapshot(), 0)
        before = h.digest(self.original)
        self.assertEqual(self.cli("move-static", "Hair", "--delta", 0.1, 0, 0, "--actor", "human", "--note", "test only"), 0)
        new = self.project / self.state()["candidate"]["path"]
        x, xb = chunks(self.original); y, yb = chunks(new)
        self.assertEqual(xb, yb)
        self.assertEqual(x["nodes"][:2], y["nodes"][:2])
        self.assertAlmostEqual(y["nodes"][2]["translation"][0], 0.1)
        self.assertEqual(h.digest(self.original), before)
        self.assertNotEqual(self.cli("deliver"), 0)

    def test_unknown_contract(self):
        p = dict(self.policy, target="production engine")
        with self.assertRaises(ValueError):
            h.policy_ok(p)


if __name__ == "__main__":
    unittest.main()
