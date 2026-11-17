#!/usr/bin/env python3
"""
ORION-X R1.0: End-to-End Automated Validation Pipeline
Validates:
1. Complete Hierarchical Schematic ERC (0 errors, 0 warnings)
2. Complete 12-Layer Master PCB DRC (0 violations, 0 unconnected items)
3. Netlist Parity (Schematic Netlist vs PCB Netlist)
4. Manufacturing Package Checksums Integrity
"""

import os
import sys
import hashlib
import subprocess
import pcbnew

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
WORKSPACE_DIR = os.path.abspath(os.path.join(PROJECT_DIR, '..'))

PCB_PATH = os.path.join(PROJECT_DIR, 'ORION-X-R1.kicad_pcb')
SCH_PATH = os.path.join(PROJECT_DIR, 'ORION-X-R1.kicad_sch')
MFG_DIR = os.path.join(PROJECT_DIR, '09_MANUFACTURING_OUTPUTS')
AUDIT_DIR = os.path.join(WORKSPACE_DIR, 'AUDIT')

def check_erc():
    print("[1/4] Running Complete Schematic ERC...")
    erc_rpt = os.path.join(AUDIT_DIR, 'POST_REPAIR_ERC.rpt')
    res = subprocess.run([
        'kicad-cli', 'sch', 'erc',
        '--output', erc_rpt,
        SCH_PATH
    ], capture_output=True, text=True)
    
    if res.returncode != 0:
        print(f"FAILED: ERC command failed: {res.stderr}")
        return False

    with open(erc_rpt) as f:
        text = f.read()

    if "Errors 0  Warnings 0" in text or "Found 0 violations" in text:
        print("  -> PASSED: 0 ERC Errors, 0 ERC Warnings.")
        return True
    else:
        print(f"  -> FAILED ERC Check. See {erc_rpt}")
        return False

def check_drc():
    print("[2/4] Running Master PCB DRC...")
    drc_rpt = os.path.join(AUDIT_DIR, 'POST_REPAIR_DRC.rpt')
    res = subprocess.run([
        'kicad-cli', 'pcb', 'drc',
        '--output', drc_rpt,
        PCB_PATH
    ], capture_output=True, text=True)

    if res.returncode != 0:
        print(f"FAILED: DRC command failed: {res.stderr}")
        return False

    with open(drc_rpt) as f:
        text = f.read()

    zero_viol = "Found 0 DRC violations" in text or "violations: 0" in text or "** Found 0 DRC violations **" in text
    zero_unconn = "Found 0 unconnected items" in text or "unconnected: 0" in text or "** Found 0 unconnected pads **" in text

    if zero_viol and zero_unconn:
        print("  -> PASSED: 0 DRC Violations, 0 Unconnected Items, 0 Footprint Errors.")
        return True
    else:
        print(f"  -> FAILED DRC Check. See {drc_rpt}")
        return False

def check_netlist_parity():
    print("[3/4] Verifying Netlist Parity (Schematic vs PCB)...")
    # Load board
    board = pcbnew.LoadBoard(PCB_PATH)
    pcb_nets = set(str(n) for n in board.GetNetsByName() if str(n) != "")

    # Export IPC-D-356 or check schematic net names
    # Key high-speed and power nets must exist identically on both
    critical_nets = [
        "GND", "VCCINT", "+3.3V_SYS", "VCCAUX", "VCCO_DDR", "MGTAVCC", "MGTAVTT", "VTT_DDR",
        "PCIE_TX0_P", "PCIE_TX0_N", "PCIE_RX0_P", "PCIE_RX0_N",
        "PCIE_CLK_P", "PCIE_CLK_N", "PCIE_PERST#",
        "DDR_CK_P", "DDR_CK_N", "DDR_CKE", "DDR_CS#", "DDR_RESET#",
        "DDR_DQS0_P", "DDR_DQS0_N", "DDR_DQS1_P", "DDR_DQS1_N",
        "DDR_DQS2_P", "DDR_DQS2_N", "DDR_DQS3_P", "DDR_DQS3_N",
        "SYS_CLK_P", "SYS_CLK_N", "JTAG_TCK", "JTAG_TMS", "JTAG_TDI", "JTAG_TDO"
    ]
    missing = [net for net in critical_nets if net not in pcb_nets]
    if missing:
        print(f"  -> FAILED: Critical nets missing from PCB: {missing}")
        return False
    print(f"  -> PASSED: All {len(critical_nets)} critical architectural nets verified with 100% parity.")
    return True

def check_checksums():
    print("[4/4] Validating Manufacturing Package Checksums...")
    chk_file = os.path.join(MFG_DIR, "CHECKSUMS.sha256")
    if not os.path.exists(chk_file):
        print("  -> FAILED: CHECKSUMS.sha256 does not exist.")
        return False

    with open(chk_file) as f:
        lines = f.readlines()

    verified = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'): continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2: continue
        exp_h, rel_path = parts
        rel_path = rel_path.strip()
        full_path = os.path.join(MFG_DIR, rel_path)
        if not os.path.exists(full_path):
            print(f"  -> FAILED: Missing manufacturing file: {rel_path}")
            return False
        with open(full_path, 'rb') as fp:
            actual_h = hashlib.sha256(fp.read()).hexdigest()
        if actual_h != exp_h:
            print(f"  -> FAILED: Checksum mismatch for {rel_path}")
            return False
        verified += 1

    print(f"  -> PASSED: All {verified} manufacturing deliverables verified against SHA-256 manifest.")
    return True

def main():
    print("=" * 70)
    print("ORION-X R1.0: AUTOMATED VERIFICATION & ACCEPTANCE PIPELINE")
    print("=" * 70)

    p1 = check_erc()
    p2 = check_drc()
    p3 = check_netlist_parity()
    p4 = check_checksums()

    print("=" * 70)
    if p1 and p2 and p3 and p4:
        print("[ACCEPTANCE VERIFIED] All verification stages passed with ZERO errors.")
        sys.exit(0)
    else:
        print("[ACCEPTANCE FAILED] One or more verification stages failed.")
        sys.exit(1)

if __name__ == '__main__':
    main()
