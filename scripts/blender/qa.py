"""Run with Blender 4.x/5.x in a new headless process; structural preview only."""
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def signature(obj):
    m = obj.data
    data = [list(map(list, obj.matrix_world)), [list(v.co) for v in m.vertices], [list(p.vertices) for p in m.polygons], [[list(d.uv) for d in u.data] for u in m.uv_layers], [x.name if x else None for x in m.materials], [[(o.vertex_groups[g.group].name, g.weight) for g in v.groups] for v in m.vertices], [(k.name, [list(v.co) for v in k.data]) for k in m.shape_keys.key_blocks] if m.shape_keys else []]
    return hashlib.sha256(json.dumps(data, separators=(",", ":")).encode()).hexdigest()


def inspect(p, protected):
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    errors = {k: [] for k in ("mesh", "topology", "uv", "material", "textures", "rig", "shapes", "protected")}
    facts = {"triangles": 0, "meshes": len(meshes), "bones": [], "shapes": []}
    sigs = {}
    if not meshes:
        errors["mesh"].append("No mesh")
    bones, shapes = set(), set()
    for o in meshes:
        m = o.data
        m.calc_loop_triangles()
        facts["triangles"] += len(m.loop_triangles)
        sigs[o.name] = signature(o)
        if not m.vertices or not m.polygons:
            errors["mesh"].append(o.name + ": empty geometry")
        if any(not all(math.isfinite(x) for x in v.co) for v in m.vertices):
            errors["mesh"].append(o.name + ": nonfinite coordinates")
        bm = bmesh.new()
        try:
            bm.from_mesh(m)
            if any(len(e.link_faces) > 2 or not e.link_faces or (e.is_manifold and not e.is_contiguous) for e in bm.edges) or any(not v.link_edges for v in bm.verts) or any(f.calc_area() <= 1e-12 for f in bm.faces):
                errors["topology"].append(o.name + ": nonmanifold/wire/winding/degenerate geometry")
            if o.name not in p["open_meshes"] and any(e.is_boundary for e in bm.edges):
                errors["topology"].append(o.name + ": unexpected open boundary")
        finally:
            bm.free()
        if p["require_uv"] and not m.uv_layers:
            errors["uv"].append(o.name + ": no UV")
        if p["require_material"] and (not m.materials or any(poly.material_index >= len(m.materials) or m.materials[poly.material_index] is None for poly in m.polygons)):
            errors["material"].append(o.name + ": unassigned material")
        for mat in m.materials:
            if mat and mat.use_nodes and mat.node_tree:
                for node in mat.node_tree.nodes:
                    if node.type == "TEX_IMAGE" and (node.image is None or (not node.image.packed_file and node.image.source == "FILE" and not Path(bpy.path.abspath(node.image.filepath)).is_file())):
                        errors["textures"].append(o.name + ": missing image in " + mat.name)
        rigs = [mod.object for mod in o.modifiers if mod.type == "ARMATURE" and mod.object and mod.object.type == "ARMATURE"]
        if p["require_rig"]:
            if not rigs:
                errors["rig"].append(o.name + ": no armature modifier")
            else:
                deform = {b.name for rig in rigs for b in rig.data.bones if b.use_deform}
                bones.update(b.name for rig in rigs for b in rig.data.bones)
                indices = {g.index for g in o.vertex_groups if g.name in deform}
                for v in m.vertices:
                    w = [g.weight for g in v.groups if g.group in indices]
                    if not w or not all(math.isfinite(x) and 0 <= x <= 1 for x in w) or abs(sum(w) - 1) > 0.01:
                        errors["rig"].append(o.name + ": missing or unnormalized deform weights")
                        break
        if m.shape_keys:
            shapes.update(x.name for x in m.shape_keys.key_blocks)
    if facts["triangles"] > p["max_triangles"]:
        errors["mesh"].append("Triangle budget exceeded")
    for name in set(p["required_bones"]) - bones:
        errors["rig"].append("Missing bone: " + name)
    for name in set(p["required_shapes"]) - shapes:
        errors["shapes"].append("Missing shape: " + name)
    for name, expected in protected.items():
        if sigs.get(name) != expected:
            errors["protected"].append("Changed protected mesh signature: " + name)
    facts.update(bones=sorted(bones), shapes=sorted(shapes))
    return {k: {"status": "FAIL" if v else "PASS", "findings": v} for k, v in errors.items()}, facts, sigs


def render_views(folder, policy, previous_frame):
    front = policy["front"]
    scene = bpy.context.scene
    pts = [o.matrix_world @ Vector(c) for o in scene.objects if o.type == "MESH" for c in o.bound_box]
    if not pts:
        return {}, None
    lo = Vector(tuple(min(v[i] for v in pts) for i in range(3)))
    hi = Vector(tuple(max(v[i] for v in pts) for i in range(3)))
    center = (lo + hi) / 2
    span = max((hi - lo).length, 0.01)
    if previous_frame:
        center, span = Vector(previous_frame["center"]), previous_frame["span"]
    frame = {"center": list(center), "span": span}
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.color_type = "MATERIAL"
    scene.render.resolution_x = scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    camera = bpy.data.objects.new("QA camera", bpy.data.cameras.new("QA camera"))
    scene.collection.objects.link(camera); scene.camera = camera
    camera.data.type = "ORTHO"; camera.data.ortho_scale = span * 1.2
    direction = Vector({"-Y": (0,-1,0), "+Y": (0,1,0), "-X": (-1,0,0), "+X": (1,0,0)}[front])
    left = Vector((direction.y, -direction.x, 0))
    result = {}
    for name, d in (("front", direction), ("left", left), ("back", -direction), ("right", -left)):
        camera.location = center + d * span * 2
        camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
        camera.data.clip_end = span * 10 + 100
        path = folder / (name + ".png")
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        result[path.name] = sha(path)
    if policy.get("face_mesh"):
        face = bpy.context.scene.objects.get(policy["face_mesh"])
        if face and face.type == "MESH":
            corners = [face.matrix_world @ Vector(c) for c in face.bound_box]
            focus = sum(corners, Vector((0, 0, 0))) / len(corners)
            size = max((v - focus).length for v in corners) * 2
            camera.data.ortho_scale = max(size * 1.2, 0.01)
            camera.location = focus + direction * max(size * 2, 0.02)
            camera.rotation_euler = (focus - camera.location).to_track_quat("-Z", "Y").to_euler()
            path = folder / "face.png"; scene.render.filepath = str(path)
            bpy.ops.render.render(write_still=True); result[path.name] = sha(path)
    if policy.get("motion_frames"):
        camera.data.ortho_scale = span * 1.2
        camera.location = center + direction * span * 2
        camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
        for f in policy["motion_frames"]:
            scene.frame_set(f)
            path = folder / ("pose_" + str(f) + ".png")
            scene.render.filepath = str(path)
            bpy.ops.render.render(write_still=True)
            result[path.name] = sha(path)
    return result, frame


def main():
    asset, folder = map(Path, sys.argv[sys.argv.index("--") + 1:])
    req = json.loads((folder / "request.json").read_text(encoding="utf-8"))
    if sha(asset) != req["asset_sha"]:
        raise ValueError("Candidate changed")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if "FINISHED" not in bpy.ops.import_scene.gltf(filepath=str(asset)):
        raise RuntimeError("GLB import did not finish")
    bpy.context.view_layer.update()
    checks, facts, sigs = inspect(req["policy"], req["protected"])
    views, frame = render_views(folder, req["policy"], req.get("frame"))
    report = {"schema": 1, "asset_sha": req["asset_sha"], "policy_sha": req["policy_sha"], "checker_sha": sha(Path(__file__)), "protected_sha": req["protected_sha"], "blender": bpy.app.version_string, "checks": checks, "facts": facts, "objects": sigs, "renders": views, "frame": frame, "limitations": "Fresh GLB import; base topology and basic structural signature only. Workbench previews not textured appearance; no visual similarity, full skin/shape deformation, collision or runtime proof."}
    (folder / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
