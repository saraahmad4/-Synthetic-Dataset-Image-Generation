import bpy
import random
import math
import os
from mathutils import Vector
N_IMAGES = 50
OUT_DIR = bpy.path.abspath("//dataset/")

os.makedirs(OUT_DIR, exist_ok=True)

car = bpy.data.objects["senna"]
cam = bpy.data.objects["Camera"]
sun = bpy.data.objects["Sun"]
scene = bpy.context.scene

for i in range(N_IMAGES):
    car.location.x = random.uniform(-20, 20)
    car.location.y = random.uniform(-10, 10)
    car.rotation_euler.z = random.uniform(0, 2 * math.pi)
    sun.rotation_euler.x = math.radians(random.uniform(20, 60))
    sun.rotation_euler.z = math.radians(random.uniform(0, 360))
    bpy.context.view_layer.update()

    corners = [
        car.matrix_world @ Vector(corner)
        for corner in car.bound_box
    ]

    from bpy_extras.object_utils import world_to_camera_view
    coords = [
        world_to_camera_view(scene, cam, point)
        for point in corners
    ]

    x0 = max(0, min(p.x for p in coords))
    x1 = min(1, max(p.x for p in coords))
    y0 = max(0, min(p.y for p in coords))
    y1 = min(1, max(p.y for p in coords))

    name = f"img_{i:03d}"
    scene.render.filepath = os.path.join(OUT_DIR, name + ".png")
    bpy.ops.render.render(write_still=True)
    with open(os.path.join(OUT_DIR, name + ".txt"), "w") as f:
        f.write(
            f"0 {(x0+x1)/2:.6f} {1-(y0+y1)/2:.6f} "
            f"{x1-x0:.6f} {y1-y0:.6f}\n"
        )

print("Dataset generation complete.")
