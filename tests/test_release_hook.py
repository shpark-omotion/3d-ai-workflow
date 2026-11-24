import subprocess
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from release_hook import evaluate


class HookTest(unittest.TestCase):
    def test_no_implicit_execution(self):
        def forbidden(*a, **kw):
            self.fail("Hook must not run")
        self.assertEqual(evaluate({}, False, "/test", forbidden), {})
        self.assertEqual(evaluate({"stop_hook_active": True}, True, "/test", forbidden), {})

    def test_gate_block_advisory(self):
        def failure(cmd, **kw):
            self.assertEqual(cmd[-1], "gate")
            return subprocess.CompletedProcess(cmd, 1)
        self.assertEqual(evaluate({}, True, "/test", failure)["decision"], "block")
