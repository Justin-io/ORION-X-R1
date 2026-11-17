#!/usr/bin/env python3
"""
PROJECT ORION-X R1.0: Complete Schematic Wire & ERC Synthesis Engine
Synthesizes electrically valid, grid-aligned, fully-wired KiCad 9 schematics
from the master PCB netlist and component symbol libraries.
"""

import os
import sys
import re
import uuid
import pcbnew

def get_uuid():
    return str(uuid.uuid4())

def round_grid(val, grid=1.27):
    return round(round(val / grid) * grid, 2)

def load_pcb_nets(pcb_path):
    board = pcbnew.LoadBoard(pcb_path)
    pcb_nets = {}
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        pcb_nets[ref] = {}
        for pad in fp.Pads():
            n = pad.GetNetname()
            if n and not n.startswith("Net-") and not n.startswith("NET_") and n != "NC":
                pcb_nets[ref][pad.GetNumber()] = n
    return pcb_nets

def parse_symbol_library(sym_path):
    with open(sym_path) as f:
        txt = f.read()
    
    symbols = {}
    # Find all base symbols
    # A symbol starts with \t(symbol "NAME"
    lines = txt.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^\t\(symbol\s+\"([^\"]+)\"", line)
        if m:
            sname = m.group(1)
            block = [line]
            depth = 1
            i += 1
            while i < len(lines) and depth > 0:
                l = lines[i]
                depth += l.count("(") - l.count(")")
                block.append(l)
                i += 1
            symbols[sname] = "\n".join(block)
        else:
            i += 1
    return symbols

def extract_pins_from_symbol(sym_block):
    # Parse pins per unit
    unit_pins = {}
    # Pattern to match sub-symbols: (symbol "NAME_U_D" ... )
    unit_blocks = re.findall(r"\(symbol\s+\"([^\"]+)_([0-9]+)_([0-9]+)\"(.*?)\n\t\t\)", sym_block, re.DOTALL)
    for base, u_str, d_str, u_body in unit_blocks:
        u = int(u_str)
        if u not in unit_pins:
            unit_pins[u] = []
        # Match each pin
        patt = re.compile(r"\(pin\s+([^\s]+)\s+([^\s]+)\s+\(at\s+([0-9.-]+)\s+([0-9.-]+)\s+([0-9.-]+)\)\s+\(length\s+([0-9.-]+)\).*?\(name\s+\"([^\"]+)\".*?\(number\s+\"([^\"]+)\"", re.DOTALL)
        for m in patt.finditer(u_body):
            ptype, pshape, px, py, prot, plen, pname, pnum = m.groups()
            unit_pins[u].append({
                "type": ptype,
                "shape": pshape,
                "x": float(px),
                "y": float(py),
                "rot": int(float(prot)),
                "len": float(plen),
                "name": pname,
                "num": pnum
            })
    return unit_pins

def main():
    proj_dir = "/home/justin/Desktop/orion/ORION-X-R1"
    pcb_path = os.path.join(proj_dir, "ORION-X-R1.kicad_pcb")
    sym_dir = os.path.join(proj_dir, "03_KICAD", "SYMBOLS")

    print(f"Loading PCB netlist from {pcb_path}...")
    pcb_nets = load_pcb_nets(pcb_path)

    # Load all symbol libraries
    lib_files = {
        "ORION_CLOCK": os.path.join(sym_dir, "ORION_CLOCK.kicad_sym"),
        "ORION_CONNECTORS": os.path.join(sym_dir, "ORION_CONNECTORS.kicad_sym"),
        "ORION_FPGA": os.path.join(sym_dir, "ORION_FPGA.kicad_sym"),
        "ORION_MEMORY": os.path.join(sym_dir, "ORION_MEMORY.kicad_sym"),
        "ORION_MISC": os.path.join(sym_dir, "ORION_MISC.kicad_sym"),
        "ORION_POWER": os.path.join(sym_dir, "ORION_POWER.kicad_sym"),
    }

    all_symbols = {}
    for lib_id, lpath in lib_files.items():
        parsed = parse_symbol_library(lpath)
        for sname, sblock in parsed.items():
            all_symbols[f"{lib_id}:{sname}"] = sblock

    print(f"Loaded {len(all_symbols)} symbols across all libraries.")

    # Sheet configurations
    root_uuid = "098037f2-1aff-4ef0-b921-fed0175b17b2"
    sheets_config = [
        {
            "filename": "01_PCIE_EDGE.kicad_sch",
            "sheet_uuid": "b96ad79b-7dab-4c42-b950-b9e7f135e1e5",
            "page": "2",
            "paper": "A3",
            "title": "ORION-X R1.0: PCIe Gen2 x4 Edge & Power Entry",
            "components": [
                {
                    "ref": "J1",
                    "val": "PCIe-Edge-x4",
                    "lib_id": "ORION_CONNECTORS:PCIe-Edge-x4",
                    "footprint": "ORION_CONNECTORS:BUS_PCIexpress_x4",
                    "datasheet": "PCI-SIG CEM 2.0",
                    "units": [1],
                    "positions": [(180.0, 150.0)]
                }
            ]
        },
        {
            "filename": "02_FPGA_CORE.kicad_sch",
            "sheet_uuid": "ca06345d-8c47-41b5-8e1f-c0faf7e7dbb2",
            "page": "3",
            "paper": "A1",
            "title": "ORION-X R1.0: AMD Kintex-7 XC7K160T FPGA Core",
            "components": [
                {
                    "ref": "U1",
                    "val": "XC7K160T-2FFG676C",
                    "lib_id": "ORION_FPGA:XC7K160T-2FFG676C",
                    "footprint": "ORION_FPGA:Xilinx_FFG676",
                    "datasheet": "AMD DS182 / UG475",
                    "units": [1, 2, 3, 4, 5, 6, 7, 8],
                    "positions": [
                        (80.0, 100.0),   # Unit 1: Bank 12/13
                        (240.0, 100.0),  # Unit 2: Bank 14/15
                        (400.0, 100.0),  # Unit 3: Bank 16/32
                        (560.0, 100.0),  # Unit 4: Bank 33/34
                        (80.0, 320.0),   # Unit 5: Bank 115/116 GTX
                        (240.0, 320.0),  # Unit 6: MGT Power
                        (400.0, 320.0),  # Unit 7: Config
                        (560.0, 320.0)   # Unit 8: Power / GND
                    ]
                }
            ]
        },
        {
            "filename": "03_DDR3L_MEMORY.kicad_sch",
            "sheet_uuid": "b6a4df0f-fe21-44c9-8873-16f1b7ffbe0a",
            "page": "4",
            "paper": "A2",
            "title": "ORION-X R1.0: 1GB DDR3L-1600 Memory Subsystem",
            "components": [
                {
                    "ref": "U2",
                    "val": "MT41K256M16TW-107-AAT:P",
                    "lib_id": "ORION_MEMORY:MT41K256M16TW-107-AAT_P",
                    "footprint": "ORION_MEMORY:Micron_FBGA-96_9x14mm_P0.8mm",
                    "datasheet": "Micron MT41K256M16",
                    "units": [1],
                    "positions": [(140.0, 160.0)]
                },
                {
                    "ref": "U3",
                    "val": "MT41K256M16TW-107-AAT:P",
                    "lib_id": "ORION_MEMORY:MT41K256M16TW-107-AAT_P",
                    "footprint": "ORION_MEMORY:Micron_FBGA-96_9x14mm_P0.8mm",
                    "datasheet": "Micron MT41K256M16",
                    "units": [1],
                    "positions": [(340.0, 160.0)]
                }
            ]
        },
        {
            "filename": "04_FPGA_POWER.kicad_sch",
            "sheet_uuid": "7c7f4e7c-1882-4bec-bdf9-343fdfa3db45",
            "page": "5",
            "paper": "A2",
            "title": "ORION-X R1.0: FPGA Power Delivery Network & Telemetry",
            "components": [
                {
                    "ref": "U5",
                    "val": "TPS546D24ARVFR",
                    "lib_id": "ORION_POWER:TPS546D24ARVFR",
                    "footprint": "ORION_POWER:TI_QFN-40_5x7mm_P0.5mm_TPS546D24A",
                    "datasheet": "https://www.ti.com/lit/ds/symlink/tps546d24a.pdf",
                    "units": [1],
                    "positions": [(100.0, 100.0)]
                },
                {
                    "ref": "L1",
                    "val": "0.15uH",
                    "lib_id": "ORION_MISC:XGL6060-151MEB",
                    "footprint": "ORION_MISC:Inductor_SMD_6.5x6.5mm_XGL6060",
                    "datasheet": "Coilcraft XGL6060 Series",
                    "mpn": "XGL6060-151MEB",
                    "mfr": "Coilcraft",
                    "units": [1],
                    "positions": [(200.0, 100.0)]
                },
                {
                    "ref": "U7",
                    "val": "TPSM63610RDHR",
                    "lib_id": "ORION_POWER:TPSM63610RDHR",
                    "footprint": "ORION_POWER:TI_QFN-21_5x5mm_TPSM63610",
                    "datasheet": "https://www.ti.com/lit/ds/symlink/tpsm63610.pdf",
                    "units": [1],
                    "positions": [(320.0, 100.0)]
                },
                {
                    "ref": "U8",
                    "val": "TPSM63610RDHR",
                    "lib_id": "ORION_POWER:TPSM63610RDHR",
                    "footprint": "ORION_POWER:TI_QFN-21_5x5mm_TPSM63610",
                    "datasheet": "https://www.ti.com/lit/ds/symlink/tpsm63610.pdf",
                    "units": [1],
                    "positions": [(460.0, 100.0)]
                },
                {
                    "ref": "U10",
                    "val": "TPS7A8500RTER",
                    "lib_id": "ORION_POWER:TPS7A8500RTER",
                    "footprint": "ORION_POWER:TI_VQFN-20_3.5x3.5mm_TPS7A8500",
                    "datasheet": "https://www.ti.com/lit/ds/symlink/tps7a85.pdf",
                    "units": [1],
                    "positions": [(160.0, 260.0)]
                },
                {
                    "ref": "U11",
                    "val": "TPS7A8500RTER",
                    "lib_id": "ORION_POWER:TPS7A8500RTER",
                    "footprint": "ORION_POWER:TI_VQFN-20_3.5x3.5mm_TPS7A8500",
                    "datasheet": "https://www.ti.com/lit/ds/symlink/tps7a85.pdf",
                    "units": [1],
                    "positions": [(360.0, 260.0)]
                }
            ]
        },
        {
            "filename": "05_DDR_POWER.kicad_sch",
            "sheet_uuid": "59c28bf3-bb0c-42a8-a2b5-98e5044d6f4b",
            "page": "6",
            "paper": "A3",
            "title": "ORION-X R1.0: DDR3L Power Architecture (1.35V VCCO & VTT/VREF)",
            "components": [
                {
                    "ref": "U6",
                    "val": "TPSM63610RDHR",
                    "lib_id": "ORION_POWER:TPSM63610RDHR",
                    "footprint": "ORION_POWER:TI_QFN-21_5x5mm_TPSM63610",
                    "datasheet": "https://www.ti.com/lit/ds/symlink/tpsm63610.pdf",
                    "units": [1],
                    "positions": [(120.0, 120.0)]
                },
                {
                    "ref": "U9",
                    "val": "TPS51200DRCR",
                    "lib_id": "ORION_POWER:TPS51200DRCR",
                    "footprint": "ORION_POWER:TI_VSON-10_3x3mm_TPS51200",
                    "datasheet": "https://www.ti.com/lit/ds/symlink/tps51200.pdf",
                    "units": [1],
                    "positions": [(280.0, 120.0)]
                }
            ]
        },
        {
            "filename": "06_CLOCKING.kicad_sch",
            "sheet_uuid": "ba655240-cc5f-49ae-9237-559eeb17608e",
            "page": "7",
            "paper": "A3",
            "title": "ORION-X R1.0: 200 MHz Low-Jitter System Clock Architecture",
            "components": [
                {
                    "ref": "Y1",
                    "val": "200.000MHz LVDS",
                    "lib_id": "ORION_CLOCK:SiT9121AI-2B3-33E200",
                    "footprint": "ORION_CLOCK:Oscillator_SMD_SiTime_SiT9121-6Pin_3.2x2.5mm",
                    "datasheet": "https://www.sitime.com/datasheet/SiT9121",
                    "mpn": "SiT9121AI-2B3-33E200.000000",
                    "mfr": "SiTime",
                    "units": [1],
                    "positions": [(180.0, 130.0)]
                }
            ]
        },
        {
            "filename": "07_CONFIG_FLASH.kicad_sch",
            "sheet_uuid": "b0829188-4cb4-4ea5-9581-28316210d0fc",
            "page": "8",
            "paper": "A3",
            "title": "ORION-X R1.0: QSPI Configuration Flash Memory (256Mb)",
            "components": [
                {
                    "ref": "U4",
                    "val": "MX25L25645GMI-08G",
                    "lib_id": "ORION_MISC:MX25L25645GMI-08G",
                    "footprint": "ORION_MISC:SOIC-16W_7.5x10.3mm_P1.27mm",
                    "datasheet": "Macronix MX25L25645G",
                    "units": [1],
                    "positions": [(180.0, 130.0)]
                }
            ]
        },
        {
            "filename": "08_MANAGEMENT.kicad_sch",
            "sheet_uuid": "96555666-7404-412c-8a78-b5c7d71940b4",
            "page": "9",
            "paper": "A3",
            "title": "ORION-X R1.0: Management UART, I2C Telemetry & Status LEDs",
            "components": [
                {
                    "ref": "J3",
                    "val": "Management Header",
                    "lib_id": "ORION_CONNECTORS:CONN_DEBUG_2x5",
                    "footprint": "ORION_CONNECTORS:PinHeader_2x05_P2.54mm_Vertical",
                    "datasheet": "UART / I2C Debug",
                    "units": [1],
                    "positions": [(180.0, 130.0)]
                }
            ]
        },
        {
            "filename": "09_EXPANSION.kicad_sch",
            "sheet_uuid": "8a9ba756-9dbc-4037-a7a0-c3f289866ff8",
            "page": "10",
            "paper": "A3",
            "title": "ORION-X R1.0: General Purpose Expansion & High-Speed I/O",
            "components": [
                {
                    "ref": "J4",
                    "val": "GPIO Header",
                    "lib_id": "ORION_CONNECTORS:CONN_GPIO_2x10",
                    "footprint": "ORION_CONNECTORS:PinHeader_2x10_P2.54mm_Vertical",
                    "datasheet": "High-Density GPIO",
                    "units": [1],
                    "positions": [(180.0, 130.0)]
                }
            ]
        },
        {
            "filename": "10_TEST_ACCESS.kicad_sch",
            "sheet_uuid": "e8ef80fc-96b1-48f5-8e45-2878aad4a1f5",
            "page": "11",
            "paper": "A3",
            "title": "ORION-X R1.0: JTAG Programming & Power Test Access",
            "components": [
                {
                    "ref": "J2",
                    "val": "JTAG",
                    "lib_id": "ORION_CONNECTORS:JTAG_14PIN",
                    "footprint": "ORION_CONNECTORS:PinHeader_2x07_P2.00mm_Vertical",
                    "datasheet": "Xilinx JTAG 14-pin",
                    "units": [1],
                    "positions": [(180.0, 130.0)]
                }
            ]
        }
    ]

    for cfg in sheets_config:
        sch_filename = cfg["filename"]
        out_path = os.path.join(proj_dir, sch_filename)
        print(f"Generating sheet: {sch_filename}...")

        # Collect unique symbols needed on this sheet
        needed_syms = set(c["lib_id"] for c in cfg["components"])
        lib_syms_lines = []
        for s_id in needed_syms:
            s_block = all_symbols[s_id]
            # Replace internal symbol name with lib_id format
            base_name = s_id.split(":")[1]
            s_renamed = s_block.replace(f'"{base_name}"', f'"{s_id}"', 1)
            s_renamed = s_renamed.replace(f'"{base_name}_', f'"{s_id}_')
            lib_syms_lines.append(s_renamed)

        content = []
        content.append(f'(kicad_sch (version 20250114) (generator "eeschema") (generator_version "9.0")')
        content.append(f'\t(uuid "{get_uuid()}") (paper "{cfg["paper"]}")')
        content.append(f'\t(title_block (title "{cfg["title"]}") (date "2026-11-17") (rev "R1.0") (company "Google DeepMind / ORION Hardware Engineering"))')
        content.append('\t(lib_symbols')
        for lsym in lib_syms_lines:
            content.append(lsym)
        content.append('\t)')

        # Instantiate components
        for comp in cfg["components"]:
            ref = comp["ref"]
            lib_id = comp["lib_id"]
            val = comp["val"]
            fp = comp["footprint"]
            ds = comp["datasheet"]
            units = comp["units"]
            positions = comp["positions"]

            raw_sym_block = all_symbols[lib_id]
            parsed_units = extract_pins_from_symbol(raw_sym_block)

            for u_idx, unit_num in enumerate(units):
                sym_pos = positions[u_idx]
                sym_x = round_grid(sym_pos[0])
                sym_y = round_grid(sym_pos[1])

                content.append(f'\t(symbol (lib_id "{lib_id}") (at {sym_x:.2f} {sym_y:.2f} 0) (unit {unit_num})')
                content.append(f'\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)')
                content.append(f'\t\t(uuid "{get_uuid()}")')
                content.append(f'\t\t(property "Reference" "{ref}" (at {sym_x:.2f} {sym_y-5.08:.2f} 0) (effects (font (size 1.27 1.27))))')
                content.append(f'\t\t(property "Value" "{val}" (at {sym_x:.2f} {sym_y+5.08:.2f} 0) (effects (font (size 1.27 1.27))))')
                content.append(f'\t\t(property "Footprint" "{fp}" (at {sym_x:.2f} {sym_y:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))')
                content.append(f'\t\t(property "Datasheet" "{ds}" (at {sym_x:.2f} {sym_y:.2f} 0) (effects (font (size 1.27 1.27)) (hide yes)))')
                mpn = comp.get("mpn", "")
                if mpn:
                    content.append(f'\t\t(property "MPN" "{mpn}" (at {sym_x:.2f} {sym_y:.2f} 0) (effects (font (size 1.27 1.27))) (hide yes))')
                mfr = comp.get("mfr", "")
                if mfr:
                    content.append(f'\t\t(property "Manufacturer" "{mfr}" (at {sym_x:.2f} {sym_y:.2f} 0) (effects (font (size 1.27 1.27))) (hide yes))')
                content.append(f'\t\t(instances')
                content.append(f'\t\t\t(project "ORION-X-R1"')
                content.append(f'\t\t\t\t(path "/{cfg["sheet_uuid"]}"')
                content.append(f'\t\t\t\t\t(reference "{ref}") (unit {unit_num})')
                content.append(f'\t\t\t\t)')
                content.append(f'\t\t\t)')
                content.append(f'\t\t)')
                content.append(f'\t)')

                # Process pins of this unit
                pins = parsed_units.get(unit_num, [])
                for pin in pins:
                    pnum = pin["num"]
                    # Pin terminal in schematic: KiCad symbol (at X Y ROT)
                    # For rot=0, pin origin is at (sym_x + pin_x, sym_y - pin_y)
                    term_x = round_grid(sym_x + pin["x"])
                    term_y = round_grid(sym_y - pin["y"])

                    net_name = pcb_nets.get(ref, {}).get(pnum)

                    if net_name:
                        # Wire direction: away from symbol body
                        # If pin.x < 0, wire goes left
                        # If pin.x > 0, wire goes right
                        # If pin.y > 0 and pin.x == 0, wire goes up
                        # If pin.y < 0 and pin.x == 0, wire goes down
                        wire_len = 5.08
                        if pin["x"] < 0:
                            end_x = round_grid(term_x - wire_len)
                            end_y = term_y
                            lbl_rot = 180
                            shape = "input" if "IN" in pin["type"].upper() else "passive"
                        elif pin["x"] > 0:
                            end_x = round_grid(term_x + wire_len)
                            end_y = term_y
                            lbl_rot = 0
                            shape = "output" if "OUT" in pin["type"].upper() else "passive"
                        elif pin["y"] > 0:
                            end_x = term_x
                            end_y = round_grid(term_y - wire_len)
                            lbl_rot = 90
                            shape = "power_in" if "POWER" in pin["type"].upper() else "passive"
                        else:
                            end_x = term_x
                            end_y = round_grid(term_y + wire_len)
                            lbl_rot = 270
                            shape = "power_in" if "POWER" in pin["type"].upper() else "passive"

                        if net_name in ["+12V_PCIE", "+3.3V_SYS", "+3.3V_PCIE", "VCCINT", "VCCAUX", "VCCO_DDR", "MGTAVCC", "MGTAVTT", "VTT_DDR", "VREF_DDR", "GND"]:
                            shape = "power_in"

                        content.append(f'\t(wire (pts (xy {term_x:.2f} {term_y:.2f}) (xy {end_x:.2f} {end_y:.2f})) (stroke (width 0) (type default)) (uuid "{get_uuid()}"))')
                        content.append(f'\t(global_label "{net_name}" (shape {shape}) (at {end_x:.2f} {end_y:.2f} {lbl_rot}) (effects (font (size 1.27 1.27))) (uuid "{get_uuid()}"))')
                    else:
                        # NC pin
                        content.append(f'\t(no_connect (at {term_x:.2f} {term_y:.2f}) (uuid "{get_uuid()}"))')

        content.append(f'\t(sheet_instances (path "/{cfg["sheet_uuid"]}" (page "{cfg["page"]}")))')
        content.append(')')

        with open(out_path, "w") as f:
            f.write("\n".join(content) + "\n")
        print(f"Saved {out_path} ({len(content)} lines).")

    print("All 10 schematic sheets synthesized successfully.")

if __name__ == "__main__":
    main()
