"""Generate original synthetic static GLBs, no provider or third-party assets."""
import argparse
import json
import struct
from pathlib import Path


def build(path, *, opened=False, hair_offset=0.0, external=False):
    # glTF coordinates (Y up). Three independent cuboids; not an artistic asset.
    xyz = [-1,-1,-1, 1,-1,-1, 1,1,-1, -1,1,-1, -1,-1,1, 1,-1,1, 1,1,1, -1,1,1]
    ids = [0,2,1,0,3,2, 4,5,6,4,6,7, 0,1,5,0,5,4, 3,7,6,3,6,2, 0,4,7,0,7,3, 1,2,6,1,6,5]
    if opened:
        ids = ids[:-6]
    binary = struct.pack("<24f", *xyz) + struct.pack("<" + "H" * len(ids), *ids)
    nodes = [
        {"name": "Body", "mesh": 0, "translation": [0,0.8,0], "scale": [0.4,0.8,0.2]},
        {"name": "Head", "mesh": 0, "translation": [0,1.95,0], "scale": [0.33,0.35,0.28]},
        {"name": "Hair", "mesh": 0, "translation": [hair_offset,2.31,0], "scale": [0.38,0.16,0.3]},
    ]
    obj = {"asset": {"version": "2.0"}, "scene": 0, "scenes": [{"nodes": [0,1,2]}], "nodes": nodes,
           "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "indices": 1}]}],
           "buffers": [{"byteLength": len(binary)}],
           "bufferViews": [{"buffer": 0, "byteOffset": 0, "byteLength": 96, "target": 34962}, {"buffer": 0, "byteOffset": 96, "byteLength": len(binary)-96, "target": 34963}],
           "accessors": [{"bufferView": 0, "componentType": 5126, "count": 8, "type": "VEC3", "min": [-1,-1,-1], "max": [1,1,1]}, {"bufferView": 1, "componentType": 5123, "count": len(ids), "type": "SCALAR"}]}
    if external:
        obj["buffers"][0]["uri"] = "external.bin"
    data = json.dumps(obj, separators=(",", ":")).encode()
    data += b" " * (-len(data) % 4)
    binary += b"\0" * (-len(binary) % 4)
    with Path(path).open("xb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 28+len(data)+len(binary)))
        f.write(struct.pack("<I4s", len(data), b"JSON") + data)
        f.write(struct.pack("<I4s", len(binary), b"BIN\0") + binary)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("output", type=Path); p.add_argument("--open", action="store_true"); p.add_argument("--hair-offset", type=float, default=0)
    a = p.parse_args(); build(a.output, opened=a.open, hair_offset=a.hair_offset)
