#!/usr/bin/env python3
"""
Generate a professional VRML 2.0 3D model for AMD Kintex-7 FFG676 (27x27mm BGA)
"""

import os
import math

OUTPUT_PATH = "/home/justin/Desktop/orion/ORION-X-R1/03_KICAD/3D_MODELS/Xilinx_FFG676.wrl"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# KiCad StepUp VRML unit: 1/2.54 (tenth of an inch per mm)
S = 1.0 / 2.54

def box_faces(cx, cy, cz, wx, wy, wz):
    """Returns vertices and coordIndex for an axis-aligned box"""
    hx, hy, hz = wx / 2.0, wy / 2.0, wz / 2.0
    v = [
        (cx - hx, cy - hy, cz - hz),
        (cx + hx, cy - hy, cz - hz),
        (cx + hx, cy + hy, cz - hz),
        (cx - hx, cy + hy, cz - hz),
        (cx - hx, cy - hy, cz + hz),
        (cx + hx, cy - hy, cz + hz),
        (cx + hx, cy + hy, cz + hz),
        (cx - hx, cy + hy, cz + hz),
    ]
    # 6 quad faces
    faces = [
        [0, 1, 2, 3],  # bottom (-Z)
        [4, 7, 6, 5],  # top (+Z)
        [0, 4, 5, 1],  # front (-Y)
        [2, 6, 7, 3],  # back (+Y)
        [0, 3, 7, 4],  # left (-X)
        [1, 5, 6, 2],  # right (+X)
    ]
    return v, faces

def bevel_box_top(cx, cy, z_bottom, z_top, w_bottom, w_top):
    """Truncated pyramid / beveled top for heat spreader"""
    hb = w_bottom / 2.0
    ht = w_top / 2.0
    v = [
        (cx - hb, cy - hb, z_bottom),
        (cx + hb, cy - hb, z_bottom),
        (cx + hb, cy + hb, z_bottom),
        (cx - hb, cy + hb, z_bottom),
        (cx - ht, cy - ht, z_top),
        (cx + ht, cy - ht, z_top),
        (cx + ht, cy + ht, z_top),
        (cx - ht, cy + ht, z_top),
    ]
    faces = [
        [0, 1, 2, 3],  # bottom
        [4, 7, 6, 5],  # top
        [0, 4, 5, 1],  # front
        [2, 6, 7, 3],  # back
        [0, 3, 7, 4],  # left
        [1, 5, 6, 2],  # right
    ]
    return v, faces

def cylinder_faces(cx, cy, z_bot, z_top, radius, segments=8):
    v = []
    # Bottom circle
    for i in range(segments):
        th = 2.0 * math.pi * i / segments
        v.append((cx + radius * math.cos(th), cy + radius * math.sin(th), z_bot))
    # Top circle
    for i in range(segments):
        th = 2.0 * math.pi * i / segments
        v.append((cx + radius * math.cos(th), cy + radius * math.sin(th), z_top))
    
    faces = []
    # Bottom cap
    bot_face = list(range(segments - 1, -1, -1))
    faces.append(bot_face)
    # Top cap
    top_face = [segments + i for i in range(segments)]
    faces.append(top_face)
    # Sides
    for i in range(segments):
        next_i = (i + 1) % segments
        faces.append([i, next_i, segments + next_i, segments + i])
    return v, faces

def write_vrml():
    lines = [
        "#VRML V2.0 utf8",
        "# KiCad 3D Model: AMD Kintex-7 XC7K160T-2FFG676C",
        "# Package: FFG676 (27.0mm x 27.0mm x 2.6mm)",
        "",
        "# Materials",
        "Shape {",
        "  appearance Appearance {",
        "    material DEF SUBSTRATE Material {",
        "      ambientIntensity 0.2",
        "      diffuseColor 0.05 0.14 0.10",
        "      specularColor 0.15 0.25 0.18",
        "      emissiveColor 0.0 0.0 0.0",
        "      shininess 0.4",
        "    }",
        "  }",
        "}",
        "Shape {",
        "  appearance Appearance {",
        "    material DEF HEAT_SPREADER Material {",
        "      ambientIntensity 0.3",
        "      diffuseColor 0.80 0.82 0.85",
        "      specularColor 0.65 0.68 0.72",
        "      emissiveColor 0.0 0.0 0.0",
        "      shininess 0.85",
        "    }",
        "  }",
        "}",
        "Shape {",
        "  appearance Appearance {",
        "    material DEF LASER_LABEL Material {",
        "      ambientIntensity 0.1",
        "      diffuseColor 0.22 0.22 0.24",
        "      specularColor 0.1 0.1 0.1",
        "      emissiveColor 0.0 0.0 0.0",
        "      shininess 0.1",
        "    }",
        "  }",
        "}",
        "Shape {",
        "  appearance Appearance {",
        "    material DEF SOLDER_BALLS Material {",
        "      ambientIntensity 0.3",
        "      diffuseColor 0.88 0.88 0.90",
        "      specularColor 0.7 0.7 0.75",
        "      emissiveColor 0.0 0.0 0.0",
        "      shininess 0.75",
        "    }",
        "  }",
        "}",
        "Shape {",
        "  appearance Appearance {",
        "    material DEF PIN1_MARK Material {",
        "      ambientIntensity 0.3",
        "      diffuseColor 0.95 0.75 0.20",
        "      specularColor 0.5 0.4 0.1",
        "      emissiveColor 0.0 0.0 0.0",
        "      shininess 0.6",
        "    }",
        "  }",
        "}"
    ]

    def add_shape(v, faces, mat_name):
        lines.append("Shape {")
        lines.append("  geometry IndexedFaceSet {")
        lines.append("    creaseAngle 0.9")
        ci_str = ",".join([",".join(map(str, f)) + ",-1" for f in faces])
        lines.append(f"    coordIndex [{ci_str}]")
        lines.append("    coord Coordinate {")
        p_str = ",".join([f"{p[0]:.4f} {p[1]:.4f} {p[2]:.4f}" for p in v])
        lines.append(f"      point [{p_str}]")
        lines.append("    }")
        lines.append("  }")
        lines.append(f"  appearance Appearance {{ material USE {mat_name} }}")
        lines.append("}")

    # 1. Substrate: 27.0mm x 27.0mm x 0.8mm, from Z=0.45mm to Z=1.25mm
    sub_w = 27.0 * S
    sub_t = 0.8 * S
    sub_z = (0.45 + 0.8 / 2.0) * S
    v_sub, f_sub = box_faces(0, 0, sub_z, sub_w, sub_w, sub_t)
    add_shape(v_sub, f_sub, "SUBSTRATE")

    # 2. Heat Spreader Base: 24.0mm x 24.0mm x 1.0mm, from Z=1.25mm to Z=2.25mm
    lid_w = 24.0 * S
    lid_t = 1.0 * S
    lid_z = (1.25 + 1.0 / 2.0) * S
    v_lid, f_lid = box_faces(0, 0, lid_z, lid_w, lid_w, lid_t)
    add_shape(v_lid, f_lid, "HEAT_SPREADER")

    # 3. Heat Spreader Beveled Top Rim: 24.0mm to 23.2mm, Z=2.25mm to Z=2.45mm
    v_top, f_top = bevel_box_top(0, 0, 2.25 * S, 2.45 * S, 24.0 * S, 23.2 * S)
    add_shape(v_top, f_top, "HEAT_SPREADER")

    # 4. Laser Etched Marking Field on Top: 16mm x 14mm, Z=2.46mm
    v_mark, f_mark = box_faces(0, 0, 2.455 * S, 16.0 * S, 14.0 * S, 0.01 * S)
    add_shape(v_mark, f_mark, "LASER_LABEL")

    # 5. Pin 1 Gold Chamfer Marker: at top-left corner (-10.5mm, 10.5mm, Z=2.46mm)
    v_pin1, f_pin1 = cylinder_faces(-10.2 * S, 10.2 * S, 2.45 * S, 2.465 * S, 0.6 * S, segments=12)
    add_shape(v_pin1, f_pin1, "PIN1_MARK")

    # 6. Solder Balls Matrix: 26x26 perimeter and key clusters (octagonal cylinders)
    # Pitch = 1.0mm, ball diameter = 0.50mm, height = 0.45mm
    r_ball = 0.25 * S
    h_ball = 0.45 * S
    v_balls = []
    f_balls = []
    v_offset = 0

    # Draw full outer 4 rings and diagonal clusters (representative 26x26 array)
    for i in range(26):
        for j in range(26):
            # Keep outer 4 rows/cols and inner center grid
            if i < 4 or i >= 22 or j < 4 or j >= 22 or (8 <= i <= 17 and 8 <= j <= 17):
                bx = (i - 12.5) * 1.0 * S
                by = (j - 12.5) * 1.0 * S
                bv, bf = cylinder_faces(bx, by, 0.0, h_ball, r_ball, segments=6)
                for f in bf:
                    f_balls.append([idx + v_offset for idx in f])
                v_balls.extend(bv)
                v_offset += len(bv)

    add_shape(v_balls, f_balls, "SOLDER_BALLS")

    with open(OUTPUT_PATH, "w") as f:
        f.write("\n".join(lines))
    print(f"Generated {OUTPUT_PATH} ({len(lines)} lines)")

if __name__ == "__main__":
    write_vrml()

