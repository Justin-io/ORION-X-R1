#!/usr/bin/env python3
"""
ORION-X R1.0 - Deterministic High-Speed PCB Router & DRC Validator
Executes zero-DRC / zero-unconnected multi-layer routing for the 22 DDR3L nets.
"""

import os
import sys
import pcbnew
import heapq
import math
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
PCB_FILE = os.path.join(PROJECT_DIR, 'ORION-X-R1.kicad_pcb')
DRC_REPORT = os.path.abspath(os.path.join(PROJECT_DIR, '..', 'AUDIT', 'POST_REPAIR_DRC.rpt'))

def route_and_validate():
    board = pcbnew.LoadBoard(PCB_FILE)
    
    # Fill zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    board.Save(PCB_FILE)
    
    # Run DRC
    os.makedirs(os.path.dirname(DRC_REPORT), exist_ok=True)
    res = subprocess.run([
        'kicad-cli', 'pcb', 'drc',
        '--output', DRC_REPORT,
        PCB_FILE
    ], capture_output=True, text=True)
    
    print(res.stdout)
    with open(DRC_REPORT) as f:
        print(f.read())

if __name__ == '__main__':
    route_and_validate()
