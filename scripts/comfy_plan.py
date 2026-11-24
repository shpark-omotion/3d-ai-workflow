"""Build a non-submitting ComfyUI API prompt from a locally supplied object_info schema."""
import argparse
import json
from pathlib import Path, PurePosixPath


def make_prompt(schema, front, views, model, texture, pbr):
    graph = {}
    def node(cls, inputs):
        info = schema[cls]; spec = info["input"]
        required = spec.get("required", {}); allowed = {**required, **spec.get("optional", {})}
        if set(required) - set(inputs) or set(inputs) - set(allowed):
            raise ValueError("Unsupported node input contract: " + cls)
        for k, val in inputs.items():
            choices = allowed[k][0]
            if isinstance(choices, list) and not isinstance(val, list) and val not in choices:
                raise ValueError("Unsupported selection: " + cls + "." + k)
        i = str(len(graph)+1); graph[i] = {"class_type": cls, "inputs": inputs}
        return i
    def image(name):
        path = PurePosixPath(name.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts or ":" in name:
            raise ValueError("Use a ComfyUI input-relative image name")
        return [node("LoadImage", {"image": str(path)}), 0]
    if not front or not set(views) <= {"left", "back", "right"}:
        raise ValueError("Front image and documented optional views only")
    args = {"mode": "multiview_to_model" if views else "image_to_model", "apikey": "", "model_version": model, "image": image(front), "texture": texture, "pbr": pbr}
    for name, file in views.items():
        args["image_" + name] = image(file)
    if schema["TripoAPIDraft"].get("output", [])[:2] != ["STRING", "MODEL_INFO"]:
        raise ValueError("Unexpected Tripo output contract")
    model_id = node("TripoAPIDraft", args)
    if not schema["Preview3D"].get("output_node"):
        raise ValueError("Compatible Preview3D not available")
    node("Preview3D", {"model_file": [model_id, 0]})
    return graph


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--schema", type=Path, required=True); p.add_argument("--front", required=True)
    for k in ("left", "back", "right"):
        p.add_argument("--" + k)
    p.add_argument("--model", default="P2-20260801"); p.add_argument("--texture", action="store_true"); p.add_argument("--pbr", action="store_true"); p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    if a.pbr and not a.texture:
        p.error("PBR requires texture")
    try:
        graph = make_prompt(json.loads(a.schema.read_text(encoding="utf-8")), a.front, {k:getattr(a,k) for k in ("left", "back", "right") if getattr(a,k)}, a.model, a.texture, a.pbr)
        with a.output.open("x", encoding="utf-8") as f:
            json.dump(graph, f, indent=2)
    except (OSError, ValueError, KeyError, TypeError) as e:
        p.error(str(e))
    print("Draft only; no submission or credit use. Review every node before external execution.")


if __name__ == "__main__":
    main()
