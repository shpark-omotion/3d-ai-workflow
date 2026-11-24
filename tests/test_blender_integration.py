"""Opt-in real Blender tests. Set OMOTION_BLENDER to an approved absolute executable."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KIT / "scripts"), str(KIT / "examples")]
import harness as h
from make_fixture import build


@unittest.skipUnless(os.getenv("OMOTION_BLENDER"), "NOT_RUN: set OMOTION_BLENDER on a verified PC")
class BlenderIntegration(unittest.TestCase):
    def run_case(self, opened=False, **overrides):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d).resolve(); project = root / "project"
            policy = dict(h.read(KIT / "examples/policy.json"), **overrides)
            p = root / "policy.json"; p.write_text(json.dumps(policy))
            asset = root / "asset.glb"; build(asset, opened=opened)
            def call(*args):
                with contextlib.redirect_stdout(io.StringIO()):
                    return h.main(["--project", str(project), *map(str,args)])
            self.assertEqual(call("init", "--policy", p), 0)
            self.assertEqual(call("snapshot", asset), 0)
            rc = call("qa", "--blender", os.environ["OMOTION_BLENDER"])
            state = h.read(project / "state.json")
            self.assertIsNotNone(state["qa"], "Blender import/render did not finish")
            q = h.read(project / state["qa"]["report"])
            return rc, q

    def test_clean(self):
        rc, q = self.run_case()
        self.assertEqual(rc, 0, q)
        self.assertEqual(len(q["renders"]), 5)

    def test_open_mesh(self):
        rc, q = self.run_case(opened=True)
        self.assertEqual(rc, 2)
        self.assertEqual(q["checks"]["topology"]["status"], "FAIL")

    def test_allowed_open_mesh(self):
        rc, q = self.run_case(opened=True, open_meshes=["Body", "Head", "Hair"])
        self.assertEqual(rc, 0, q)

    def test_missing_contract(self):
        rc, q = self.run_case(require_uv=True, require_material=True, require_rig=True, required_bones=["root"], required_shapes=["blink"], max_triangles=1)
        self.assertEqual(rc, 2)
        for k in ("mesh", "uv", "material", "rig", "shapes"):
            self.assertEqual(q["checks"][k]["status"], "FAIL", q)
