#!/usr/bin/env python3
"""
Update all footprint 3D model paths in ORION-X-R1.kicad_pcb
"""

import pcbnew
import os

PCB_PATH = "/home/justin/Desktop/orion/ORION-X-R1/ORION-X-R1.kicad_pcb"
board = pcbnew.LoadBoard(PCB_PATH)

MODEL_MAP = {
    "U1": "/home/justin/Desktop/orion/ORION-X-R1/03_KICAD/3D_MODELS/Xilinx_FFG676.wrl",
    "U2": "${KICAD9_3DMODEL_DIR}/Package_BGA.3dshapes/BGA-96_9.0x13.0mm_Layout2x3x16_P0.8mm.wrl",
    "U3": "${KICAD9_3DMODEL_DIR}/Package_BGA.3dshapes/BGA-96_9.0x13.0mm_Layout2x3x16_P0.8mm.wrl",
    "U4": "${KICAD9_3DMODEL_DIR}/Package_SO.3dshapes/SOIC-16W_7.5x10.3mm_P1.27mm.wrl",
    "U5": "${KICAD9_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/WQFN-38-1EP_5x7mm_P0.5mm_EP3.15x5.15mm.wrl",
    "U6": "${KICAD9_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/Texas_RGY_R-PVQFN-N20_EP2.05x3.05mm.wrl",
    "U7": "${KICAD9_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/Texas_RGY_R-PVQFN-N20_EP2.05x3.05mm.wrl",
    "U8": "${KICAD9_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/Texas_RGY_R-PVQFN-N20_EP2.05x3.05mm.wrl",
    "U9": "${KICAD9_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/DFN-10-1EP_3x3mm_P0.5mm_EP1.65x2.38mm.wrl",
    "U10": "${KICAD9_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/Texas_VQFN-RGR-20-1EP_3.5x3.5mm_Pitch0.5mm.wrl",
    "U11": "${KICAD9_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/Texas_VQFN-RGR-20-1EP_3.5x3.5mm_Pitch0.5mm.wrl",
    "L1": "${KICAD9_3DMODEL_DIR}/Inductor_SMD.3dshapes/L_Bourns_SRP6060FA.wrl",
    "Y1": "${KICAD9_3DMODEL_DIR}/Crystal.3dshapes/Crystal_SMD_3225-4Pin_3.2x2.5mm.wrl",
    "J2": "${KICAD9_3DMODEL_DIR}/Connector_PinHeader_2.00mm.3dshapes/PinHeader_2x07_P2.00mm_Vertical.wrl",
    "J3": "${KICAD9_3DMODEL_DIR}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_2x05_P2.54mm_Vertical.wrl",
    "J4": "${KICAD9_3DMODEL_DIR}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_2x10_P2.54mm_Vertical.wrl"
}

for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref in MODEL_MAP:
        models = fp.Models()
        target_path = MODEL_MAP[ref]
        if len(models) == 0:
            m = pcbnew.FP_3DMODEL()
            m.m_Filename = target_path
            fp.Add3DModel(m)
            print(f"Added model for {ref}: {target_path}")
        else:
            models[0].m_Filename = target_path
            print(f"Updated model for {ref}: {target_path}")

pcbnew.SaveBoard(PCB_PATH, board)
print("Board saved with updated 3D models.")
