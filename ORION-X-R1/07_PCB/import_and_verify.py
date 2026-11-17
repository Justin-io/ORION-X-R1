#!/usr/bin/env python3
"""
ORION-X R1: Post-Routing Import, Zone Refill, DRC & Manufacturing Generation
"""

import sys
import os
import subprocess
import pcbnew

PCB_PATH = "/home/justin/Desktop/orion/ORION-X-R1/ORION-X-R1.kicad_pcb"
SES_PATH = "/tmp/orion_complete_base.ses"
PROJECT_DIR = "/home/justin/Desktop/orion/ORION-X-R1"

def import_ses_and_save():
    if not os.path.exists(SES_PATH):
        print(f"Error: {SES_PATH} not found.")
        return False

    print(f"Loading PCB: {PCB_PATH}")
    board = pcbnew.LoadBoard(PCB_PATH)

    print(f"Importing SES: {SES_PATH}")
    success = pcbnew.ImportSpecctraSES(board, SES_PATH)
    if not success:
        print("Failed to import Specctra SES.")
        return False

    print("Refilling all zones across 12 layers...")
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    print(f"Saving updated PCB: {PCB_PATH}")
    pcbnew.SaveBoard(PCB_PATH, board)
    print("PCB successfully updated and saved.")
    return True

def run_drc():
    drc_rpt = os.path.join(PROJECT_DIR, "08_VERIFICATION/DRC/DRC_REPORT.rpt")
    drc_json = os.path.join(PROJECT_DIR, "08_VERIFICATION/DRC/DRC_REPORT.json")
    os.makedirs(os.path.dirname(drc_rpt), exist_ok=True)
    
    cmd = [
        "kicad-cli", "pcb", "drc",
        "--output", drc_rpt,
        "--format", "report",
        PCB_PATH
    ]
    print(f"Running DRC: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("DRC Stderr:", res.stderr)

    cmd_json = [
        "kicad-cli", "pcb", "drc",
        "--output", drc_json,
        "--format", "json",
        PCB_PATH
    ]
    subprocess.run(cmd_json, capture_output=True, text=True)
    print(f"DRC completed. Report written to {drc_rpt}")

def generate_manufacturing():
    print("Generating Manufacturing Outputs...")
    # 1. Gerbers
    gerber_dir = os.path.join(PROJECT_DIR, "09_MANUFACTURING_OUTPUTS/GERBER/")
    os.makedirs(gerber_dir, exist_ok=True)
    cmd_gerber = [
        "kicad-cli", "pcb", "export", "gerbers",
        "--output", gerber_dir,
        "--layers", "F.Cu,In1.Cu,In2.Cu,In3.Cu,In4.Cu,In5.Cu,In6.Cu,In7.Cu,In8.Cu,In9.Cu,In10.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
        PCB_PATH
    ]
    print("Exporting Gerbers...")
    subprocess.run(cmd_gerber, check=True)

    # 2. Drill
    drill_dir = os.path.join(PROJECT_DIR, "09_MANUFACTURING_OUTPUTS/DRILL/")
    os.makedirs(drill_dir, exist_ok=True)
    cmd_drill = [
        "kicad-cli", "pcb", "export", "drill",
        "--output", drill_dir,
        "--format", "excellon",
        "--drill-origin", "absolute",
        "--excellon-separate-th",
        PCB_PATH
    ]
    print("Exporting Drill files...")
    subprocess.run(cmd_drill, check=True)

    # 3. Position (Pick and Place)
    pos_dir = os.path.join(PROJECT_DIR, "09_MANUFACTURING_OUTPUTS/PICK_AND_PLACE/")
    os.makedirs(pos_dir, exist_ok=True)
    pos_file = os.path.join(pos_dir, "ORION-X-R1-pos.csv")
    cmd_pos = [
        "kicad-cli", "pcb", "export", "pos",
        "--side", "both",
        "--format", "csv",
        "--units", "mm",
        "--output", pos_file,
        PCB_PATH
    ]
    print("Exporting Centroid Pick-and-Place...")
    subprocess.run(cmd_pos, check=True)

    # 4. BOM
    bom_dir = os.path.join(PROJECT_DIR, "09_MANUFACTURING_OUTPUTS/BOM/")
    os.makedirs(bom_dir, exist_ok=True)
    bom_file = os.path.join(bom_dir, "BOM_ORION-X-R1.csv")
    sch_path = os.path.join(PROJECT_DIR, "ORION-X-R1.kicad_sch")
    cmd_bom = [
        "kicad-cli", "sch", "export", "bom",
        "--output", bom_file,
        sch_path
    ]
    print("Exporting BOM...")
    subprocess.run(cmd_bom, check=True)

    # 5. 3D Renders
    vis_dir = os.path.join(PROJECT_DIR, "10_VISUALIZATION/")
    renders_dir = os.path.join(vis_dir, "RENDERS")
    os.makedirs(renders_dir, exist_ok=True)
    
    top_render = os.path.join(renders_dir, "ORION-X-R1_TOP.png")
    bot_render = os.path.join(renders_dir, "ORION-X-R1_BOTTOM.png")
    iso_render = os.path.join(renders_dir, "ORION-X-R1_PERSPECTIVE.png")

    print("Rendering 3D Top View...")
    subprocess.run([
        "kicad-cli", "pcb", "render",
        "--side", "top",
        "--view", "orthographic",
        "--width", "1920", "--height", "1080",
        "--output", top_render,
        PCB_PATH
    ], check=True)

    print("Rendering 3D Bottom View...")
    subprocess.run([
        "kicad-cli", "pcb", "render",
        "--side", "bottom",
        "--view", "orthographic",
        "--width", "1920", "--height", "1080",
        "--output", bot_render,
        PCB_PATH
    ], check=True)

    print("Rendering 3D Isometric View...")
    subprocess.run([
        "kicad-cli", "pcb", "render",
        "--side", "top",
        "--width", "1920", "--height", "1080",
        "--output", iso_render,
        PCB_PATH
    ], check=True)

    print("All manufacturing outputs and renders generated successfully.")

if __name__ == "__main__":
    if import_ses_and_save():
        run_drc()
        generate_manufacturing()

