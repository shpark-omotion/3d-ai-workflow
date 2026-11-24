import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from comfy_plan import make_prompt


def schema():
    return {"LoadImage": {"input": {"required": {"image": [["front.png", "back.png"]]}}}, "TripoAPIDraft": {"input": {"required": {"mode": [["image_to_model", "multiview_to_model"]], "apikey": ["STRING"]}, "optional": {"model_version": [["P2-20260801"]], "image": ["IMAGE"], "image_back": ["IMAGE"], "texture": ["BOOLEAN"], "pbr": ["BOOLEAN"]}}, "output": ["STRING", "MODEL_INFO"]}, "Preview3D": {"input": {"required": {"model_file": ["STRING"]}}, "output_node": True}}


class ComfyPlan(unittest.TestCase):
    def test_single_and_multi(self):
        graph = make_prompt(schema(), "front.png", {}, "P2-20260801", False, False)
        self.assertEqual(graph["2"]["inputs"]["apikey"], "")
        self.assertEqual(graph["3"]["inputs"]["model_file"], ["2", 0])
        graph = make_prompt(schema(), "front.png", {"back":"back.png"}, "P2-20260801", True, True)
        self.assertEqual(graph["3"]["inputs"]["mode"], "multiview_to_model")
        self.assertEqual(graph["3"]["inputs"]["image_back"], ["2",0])

    def test_schema_drift_and_bad_path(self):
        s = schema(); s["TripoAPIDraft"]["input"]["required"]["new_required"] = ["STRING"]
        with self.assertRaises(ValueError):
            make_prompt(s, "front.png", {}, "P2-20260801", False, False)
        with self.assertRaises(ValueError):
            make_prompt(schema(), "../front.png", {}, "P2-20260801", False, False)
