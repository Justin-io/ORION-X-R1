#!/usr/bin/env python3
"""
ORION-X R1.0: Authoritative Digital Manufacturing Package Generator
Produces 12-layer Gerbers, Excellon Drills, IPC-D-356 Netlist, Pick-and-Place,
BOM CSV with exact MPNs, 3D Renders, and SHA-256 Checksums.
"""

import os
import sys
import hashlib
import subprocess
import pcbnew

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
PCB_PATH = os.path.join(PROJECT_DIR, 'ORION-X-R1.kicad_pcb')
SCH_PATH = os.path.join(PROJECT_DIR, 'ORION-X-R1.kicad_sch')
MFG_DIR = os.path.join(PROJECT_DIR, '09_MANUFACTURING_OUTPUTS')

def run_command(cmd, desc):
    print(f"[*] {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"ERROR: {desc} failed!")
        print(res.stderr)
        sys.exit(1)
    return res.stdout

def main():
    print("=" * 70)
    print("ORION-X R1.0: DIGITAL MANUFACTURING PACKAGE GENERATION")
    print("=" * 70)

    # Ensure clean board & zone fills
    board = pcbnew.LoadBoard(PCB_PATH)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    board.Save(PCB_PATH)

    # 1. Gerbers
    gerber_dir = os.path.join(MFG_DIR, "GERBER")
    os.makedirs(gerber_dir, exist_ok=True)
    layers = "F.Cu,In1.Cu,In2.Cu,In3.Cu,In4.Cu,In5.Cu,In6.Cu,In7.Cu,In8.Cu,In9.Cu,In10.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts"
    run_command([
        "kicad-cli", "pcb", "export", "gerbers",
        "--output", gerber_dir + "/",
        "--layers", layers,
        PCB_PATH
    ], "Exporting 12-Layer Gerbers and Mechanical Masks")

    # 2. Drill Files
    drill_dir = os.path.join(MFG_DIR, "DRILL")
    os.makedirs(drill_dir, exist_ok=True)
    run_command([
        "kicad-cli", "pcb", "export", "drill",
        "--output", drill_dir + "/",
        "--format", "excellon",
        "--drill-origin", "absolute",
        "--excellon-separate-th",
        PCB_PATH
    ], "Exporting Excellon PTH & NPTH Drill Files")

    # 3. IPC-D-356 Electrical Test Netlist
    ipcd_dir = os.path.join(MFG_DIR, "IPC-D-356")
    os.makedirs(ipcd_dir, exist_ok=True)
    ipcd_file = os.path.join(ipcd_dir, "ORION-X-R1.d356")
    run_command([
        "kicad-cli", "pcb", "export", "ipcd356",
        "--output", ipcd_file,
        PCB_PATH
    ], "Exporting IPC-D-356 Electrical Test Netlist")

    # 4. Centroid Pick-and-Place
    pos_dir = os.path.join(MFG_DIR, "PICK_AND_PLACE")
    os.makedirs(pos_dir, exist_ok=True)
    pos_file = os.path.join(pos_dir, "ORION-X-R1-pos.csv")
    run_command([
        "kicad-cli", "pcb", "export", "pos",
        "--side", "both",
        "--format", "csv",
        "--units", "mm",
        "--output", pos_file,
        PCB_PATH
    ], "Exporting Centroid Pick-and-Place CSV")

    # 5. Bill of Materials (BOM)
    bom_dir = os.path.join(MFG_DIR, "BOM")
    os.makedirs(bom_dir, exist_ok=True)
    bom_file = os.path.join(bom_dir, "BOM_ORION-X-R1.csv")
    if not os.path.exists(bom_file) or os.path.getsize(bom_file) < 100:
        run_command([
            "kicad-cli", "sch", "export", "bom",
            "--output", bom_file,
            SCH_PATH
        ], "Exporting BOM CSV from Schematics")
    else:
        print("[*] Authoritative Comprehensive BOM verified present.")

    # 6. 3D Renders
    vis_dir = os.path.join(PROJECT_DIR, "10_VISUALIZATION", "RENDERS")
    os.makedirs(vis_dir, exist_ok=True)
    top_render = os.path.join(vis_dir, "ORION-X-R1_TOP.png")
    bot_render = os.path.join(vis_dir, "ORION-X-R1_BOTTOM.png")
    iso_render = os.path.join(vis_dir, "ORION-X-R1_PERSPECTIVE.png")

    run_command([
        "kicad-cli", "pcb", "render",
        "--side", "top",
        "--width", "1920", "--height", "1080",
        "--output", top_render,
        PCB_PATH
    ], "Rendering 3D Top View (1080p)")

    run_command([
        "kicad-cli", "pcb", "render",
        "--side", "bottom",
        "--width", "1920", "--height", "1080",
        "--output", bot_render,
        PCB_PATH
    ], "Rendering 3D Bottom View (1080p)")

    run_command([
        "kicad-cli", "pcb", "render",
        "--side", "top",
        "--perspective",
        "--rotate", "45,0,45",
        "--width", "1920", "--height", "1080",
        "--output", iso_render,
        PCB_PATH
    ], "Rendering 3D Isometric View (1080p)")

    # 7. Checksums
    checksum_file = os.path.join(MFG_DIR, "CHECKSUMS.sha256")
    print("[*] Generating SHA-256 Checksums...")
    lines = []
    for root, dirs, files in sorted(os.walk(MFG_DIR)):
        for f in sorted(files):
            if f == "CHECKSUMS.sha256": continue
            filepath = os.path.join(root, f)
            relpath = os.path.relpath(filepath, MFG_DIR)
            with open(filepath, 'rb') as fp:
                h = hashlib.sha256(fp.read()).hexdigest()
            lines.append(f"{h}  {relpath}\n")

    with open(checksum_file, 'w') as fp:
        fp.writelines(lines)
    print(f"Generated checksums for {len(lines)} manufacturing files.")
    print("\n[SUCCESS] Authoritative Manufacturing Package generated.")

if __name__ == '__main__':
    main()
