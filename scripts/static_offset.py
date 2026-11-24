"""Conservative static GLB root-node translation. No rig, morph, animation or extension support."""
import copy
import json
import math
import struct
from pathlib import Path


def move(source, destination, node_name, delta):
    from harness import check_glb, require
    check_glb(source)
    raw = source.read_bytes()
    n = struct.unpack_from("<I", raw, 12)[0]
    document = json.loads(raw[20:20+n])
    require(not any(document.get(k) for k in ("skins", "animations", "extensionsUsed", "extensionsRequired")), "Static non-extended GLB only")
    require(not any(p.get("targets") for m in document.get("meshes", []) for p in m.get("primitives", [])), "Morph targets not supported")
    nodes = document.get("nodes", [])
    matches = [i for i, node in enumerate(nodes) if node.get("name") == node_name]
    require(len(matches) == 1, "Unique node name required")
    i = matches[0]; node = nodes[i]
    require(any(i in scene.get("nodes", []) for scene in document.get("scenes", [])), "Node must be a scene root")
    require("mesh" in node and not node.get("children") and "matrix" not in node and not any(i in x.get("children", []) for x in nodes), "Only independent root mesh nodes")
    require(len(delta) == 3 and all(math.isfinite(x) for x in delta), "Finite xyz delta required")
    before = copy.deepcopy(document)
    original = node.get("translation", [0,0,0])
    node["translation"] = [x + y for x,y in zip(original, delta)]
    require(all(math.isfinite(x) for x in node["translation"]), "Invalid result")
    expected = copy.deepcopy(before); expected["nodes"][i]["translation"] = node["translation"]
    require(document == expected, "Unexpected changes")
    payload = json.dumps(document, separators=(",", ":"), ensure_ascii=False).encode()
    payload += b" " * (-len(payload) % 4)
    rest = raw[20+n:]
    output = struct.pack("<4sII", b"glTF", 2, 20+len(payload)+len(rest)) + struct.pack("<I4s", len(payload), b"JSON") + payload + rest
    with Path(destination).open("xb") as f:
        f.write(output)
    check_glb(destination)
    return {"node": node_name, "before": original, "after": node["translation"], "other_json_fields_preserved": True, "binary_chunks_preserved": True}
