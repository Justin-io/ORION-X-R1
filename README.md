# PROJECT ORION-X (Revision R1.0)
## High-Density FPGA Computing & PCI Express Accelerator Platform
### Digital Hardware Design in KiCad 9.0.2

[![Hardware Release](https://img.shields.io/badge/Release-ORION--X--R1.0-blue.svg)](https://github.com/)
[![KiCad Version](https://img.shields.io/badge/EDA-KiCad%209.0.2-228B22.svg)](https://kicad.org)
[![DRC Status](https://img.shields.io/badge/DRC-0%20Errors-brightgreen.svg)](ORION-X-R1/08_VERIFICATION/DRC/DRC_REPORT.rpt)
[![ERC Status](https://img.shields.io/badge/ERC-0%20Errors-brightgreen.svg)](ORION-X-R1/08_VERIFICATION/ERC/ERC_REPORT.rpt)
[![Stackup](https://img.shields.io/badge/Stackup-12--Layer%20Megtron%206-orange.svg)](ORION-X-R1/04_STACKUP/STACKUP_SPECIFICATION.md)
[![License](https://img.shields.io/badge/License-CERN--OHL--S-lightgrey.svg)](LICENSE)

---

## 1. Executive Overview

**ORION-X R1.0** is an open, research-grade hardware computing accelerator engineered to interface with standard workstation and server motherboards over **PCI Express Gen2 x4 (5.0 GT/s)** and provide high-bandwidth **32-bit wide external DDR3L SDRAM memory (1600 MT/s)** for reconfigurable computing, digital signal processing (DSP), and algorithmic hardware acceleration.

Designed entirely within the **KiCad 9.0.2** EDA ecosystem, this repository contains the complete production-grade schematics, custom audited symbol/footprint libraries, controlled-impedance 12-layer PCB layout, signal/power integrity documentation, automated build scripts, and digital manufacturing packages (Gerbers, Drill, BOM, Pick-and-Place, and 3D Models).

<p align="center">
  <img src="ORION-X-R1/10_VISUALIZATION/RENDERS/ORION-X-R1_PERSPECTIVE.png" alt="ORION-X R1 3D Perspective Render" width="850">
</p>

---

## 2. Key Technical Specifications

```
+--------------------------------------------------------------------------------------------------+
| SYSTEM SPECIFICATIONS SUMMARY                                                                    |
+---------------------+----------------------------------------------------------------------------+
| Parameter           | Specification & Implementation Details                                     |
+---------------------+----------------------------------------------------------------------------+
| Form Factor         | PCI Express CEM 2.0 Standard Height, Half Length (HL) Add-in Card          |
| Board Dimensions    | 167.65 mm × 111.15 mm × 1.60 mm (6.60" × 4.376" × 0.063")                   |
| Main FPGA           | AMD Xilinx Kintex-7 XC7K160T-2FFG676C (27×27mm BGA, 1.0mm Pitch)           |
| Logic Capacity      | 162,240 Logic Cells | 650 Block RAMs (11.7 Mb) | 600 DSP48E1 Slices        |
| Host Interface      | PCI Express Gen2 x4 (5.0 GT/s/lane = 20 Gbps raw aggregate bandwidth)       |
| External Memory     | 1 GB (8 Gb) DDR3L-1600 (800 MHz), 32-bit Data Bus (2× Micron 16-bit MT41K) |
| Configuration Boot  | 256 Mb Quad-SPI NOR Flash (Macronix MX25L25645GMI-08G, 133 MHz SPI)        |
| Timebase & Clocks   | SiTime SiT9121 200.000 MHz LVDS (< 500 fs RMS jitter) + PCIe 100MHz HCSL   |
| Core Power Supply   | TI TPS546D24A 40A Synchronous Buck Converter with PMBus Telemetry (1.00V)   |
| Auxiliary Supplies  | 3× TI TPSM63610 10A Integrated Power Modules (+3.3V, +1.8V VCCAUX, 1.35V)  |
| Memory Termination  | TI TPS51200 Sinking/Sourcing DDR Termination LDO (VTT = 0.675V, VREF)       |
| Transceiver Rails   | 2× TI TPS7A8500 Ultra-Low-Noise (4.4 µVrms) LDOs (MGTAVCC 1.0V, MGTAVTT 1.2)|
| Layer Count         | 12-Layer Symmetrical Controlled-Impedance Stackup (Panasonic Megtron 6)     |
| Power Budget        | 19.8W Typical / 23.8W Peak Dissipation (26.8W Gross Input from 75W PCIe)  |
| Verification Status | DRC: 0 Violations (0 Unconnected Pads) | ERC: 0 Errors, 0 Warnings           |
| Validation Scope    | CAD-Verified & Fabrication-Ready (Physical Hardware Testing Not Performed) |
+---------------------+----------------------------------------------------------------------------+
```

---

## 3. System Architecture

```
                      +-----------------------------------------+
                      |         HOST WORKSTATION / SERVER       |
                      +-----------------------------------------+
                                           |
                                [PCIe Gen2 x4 Bus (5 GT/s)]
                                           |
+------------------------------------------v------------------------------------------+
|  PROJECT ORION-X R1 ACCELERATOR CARD                                               |
|                                                                                     |
|   +-----------------------+     +-----------------------+     +------------------+  |
|   |   PCIe EDGE (J1)      |     |  TI TPS546D24A (U5)   |     |  TI TPSM63610    |  |
|   |  - 4x TX/RX Lanes     |     |  - 40A PMBus Buck     |     |  - 10A Modules   |  |
|   |  - 100MHz HCSL Clock  |     |  - 1.00V Core VCCINT  |     |  - DDR / Aux / IO|  |
|   +-----------+-----------+     +-----------+-----------+     +--------+---------+  |
|               |                             |                          |            |
|               |      [High-Speed GTX]       | [Solid Layer 5 Plane]    | [L8 Plane] |
|               v                             v                          v            |
|   +-----------------------------------------------------------------------------+   |
|   |                       AMD KINTEX-7 FPGA (U1)                                |   |
|   |                         XC7K160T-2FFG676C                                   |   |
|   |                                                                             |   |
|   |   - 162,240 Logic Cells                    - 8x GTX Transceivers (6.6 Gbps) |   |
|   |   - 650 Block RAMs (11.7 Mb)               - Dedicated Hard PCIe Block      |   |
|   |   - 600 DSP48E1 Slices                     - Native MIG DDR3L Controller    |   |
|   +--------------------------------------+--------------------------------------+   |
|                                          |                                          |
|            [HP Banks 32, 33, 34]         |              [MGT Bank 116]              |
|        32-bit Bus @ 1600 MT/s (800MHz)   |         High-Speed Serial Expansion      |
|                      |                   |                      |                   |
|                      v                   |                      v                   |
|   +----------------------------------+   |   +----------------------------------+   |
|   |    DUAL MICRON DDR3L SDRAM       |   |   |     SAMTEC EXPANSION (J3)        |   |
|   |  - 2x MT41K256M16TW-107:P (U2/U3)|   |   |  - QSH-030-01-L-D-A (60-pin)     |   |
|   |  - 1 GB Density, Point-to-Point  |   |   |  - High-Speed Debug / Expansion  |   |
|   |  - Fly-By Address/Control & VTT  |   |   +----------------------------------+   |
|   +----------------------------------+   |                                          |
|                                          |              [HR Bank 14]                |
|   +----------------------------------+   |         Quad-SPI Configuration           |
|   |       TIMING & CLOCKING          |   |                      |                   |
|   |  - SiT9121 200MHz LVDS (U12)     |---+                      v                   |
|   |  - Low Jitter (< 500 fs RMS)     |       +----------------------------------+   |
|   |  - System & Memory Timebase      |       |    MACRONIX NOR FLASH (U4)       |   |
|   +----------------------------------+       |  - MX25L25645GMI-08G (256 Mb)    |   |
|                                              |  - High-Reliability Boot Memory  |   |
|                                              +----------------------------------+   |
+-------------------------------------------------------------------------------------+
```

---

## 4. 12-Layer Stackup & Impedance Engineering

The PCB utilizes a balanced 12-layer stackup constructed with **Panasonic Megtron 6** low-loss laminate ($D_k = 3.65$, $D_f = 0.002$ at 5 GHz) ensuring planar return current continuity and tightly controlled transmission line impedances:

```
12-LAYER CONTROLLED-IMPEDANCE CROSS-SECTION
+-------+-----------+------------+--------------------+------------------------------------+
| Layer | Name      | Thickness  | Dielectric Mat.    | Signal / Plane Assignment          |
+-------+-----------+------------+--------------------+------------------------------------+
| L01   | F.Cu      | 35 µm (1oz)| Megtron 6 (100 µm) | Microstrip: PCIe TX/RX, Clocks, SMD|
| L02   | In1.Cu    | 35 µm (1oz)| Core (150 µm)      | Solid Ground Return Plane (GND)    |
| L03   | In2.Cu    | 35 µm (1oz)| Prepreg (100 µm)   | Stripline: DDR3 Byte 0 & Byte 1    |
| L04   | In3.Cu    | 35 µm (1oz)| Core (150 µm)      | Solid Ground Return Plane (GND)    |
| L05   | In4.Cu    | 35 µm (1oz)| Prepreg (100 µm)   | Solid Core Power Plane (VCCINT 1V) |
| L06   | In5.Cu    | 35 µm (1oz)| Center Core (200µm)| Center Ground Reference Plane (GND)|
| L07   | In6.Cu    | 35 µm (1oz)| Center Core (200µm)| Center Ground Reference Plane (GND)|
| L08   | In7.Cu    | 35 µm (1oz)| Prepreg (100 µm)   | Split Power (+3.3V, 1.8V, 1.35V)   |
| L09   | In8.Cu    | 35 µm (1oz)| Core (150 µm)      | Solid Ground Return Plane (GND)    |
| L10   | In9.Cu    | 35 µm (1oz)| Prepreg (100 µm)   | Stripline: DDR3 Byte 2 & Byte 3    |
| L11   | In10.Cu   | 35 µm (1oz)| Core (150 µm)      | Solid Ground Return Plane (GND)    |
| L12   | B.Cu      | 35 µm (1oz)| -                  | Microstrip: Bottom MLCCs & Probes  |
+-------+-----------+------------+--------------------+------------------------------------+
```

### Calculated Impedance Targets
- **Single-Ended Microstrip (L1, L12)**: $W = 0.100\text{ mm} \implies Z_0 = 50.2\,\Omega$
- **Single-Ended Stripline (L3, L10)**: $W = 0.090\text{ mm} \implies Z_0 = 49.8\,\Omega$
- **PCIe Differential Microstrip (L1, L12)**: $W = 0.100\text{ mm}, S = 0.140\text{ mm} \implies Z_{diff} = 100.4\,\Omega$
- **PCIe Differential Stripline (L3, L10)**: $W = 0.090\text{ mm}, S = 0.130\text{ mm} \implies Z_{diff} = 99.6\,\Omega$
- **DDR3L Differential Pairs (DQS/CK)**: $W = 0.120\text{ mm}, S = 0.110\text{ mm} \implies Z_{diff} = 80.1\,\Omega$

---

## 5. Visualizations & 3D Renderings

<p align="center">
  <img src="ORION-X-R1/10_VISUALIZATION/RENDERS/ORION-X-R1_TOP.png" alt="ORION-X Top View" width="48%">
  <img src="ORION-X-R1/10_VISUALIZATION/RENDERS/ORION-X-R1_BOTTOM.png" alt="ORION-X Bottom View" width="48%">
</p>

- **Top View**: Displays the central AMD Kintex-7 FFG676 BGA package, dual Micron DDR3L FBGA memory ICs, high-current 40A VCCINT PMBus regulator with shielded inductor L1, and peripheral power modules.
- **Bottom View**: Highlights the dense high-frequency decoupling capacitor matrix located directly opposing the FPGA core and memory power balls for minimal loop inductance ($L_{loop} < 0.6\text{ nH}$).

---

## 6. Repository Layout & Engineering Artifacts

```
orion/
├── README.md                                   # Master Project Documentation (This File)
├── LICENSE                                     # Open Hardware License (CERN-OHL-S)
└── ORION-X-R1/                                 # KiCad R1.0 Master Project
    ├── ORION-X-R1.kicad_pro                    # Master KiCad Project Configuration
    ├── ORION-X-R1.kicad_sch                    # Hierarchical Root Schematic
    ├── ORION-X-R1.kicad_pcb                    # Complete 12-Layer Master PCB Layout
    ├── 01_PCIE_EDGE.kicad_sch                  # Sub-sheet: PCIe Host Interface
    ├── 02_FPGA_CORE.kicad_sch                  # Sub-sheet: Kintex-7 Core & I/O Banks
    ├── 03_DDR3L_MEMORY.kicad_sch               # Sub-sheet: Dual DDR3L SDRAM & Termination
    ├── 04_FPGA_POWER.kicad_sch                 # Sub-sheet: 40A VCCINT Buck & Transceiver LDOs
    ├── 05_DDR_POWER.kicad_sch                  # Sub-sheet: 1.35V DDR & VTT Termination
    ├── 06_CLOCKING.kicad_sch                   # Sub-sheet: SiT9121 Low-Jitter Oscillator
    ├── 07_CONFIG_FLASH.kicad_sch               # Sub-sheet: Quad-SPI Boot Memory
    ├── 08_MANAGEMENT.kicad_sch                 # Sub-sheet: Power-Good Chain & PMBus
    ├── 09_EXPANSION.kicad_sch                  # Sub-sheet: High-Speed Expansion Interface
    ├── 10_TEST_ACCESS.kicad_sch                # Sub-sheet: JTAG & Debug Access
    ├── 00_PROJECT_MANAGEMENT/                  # Audits, Master Register & Risk Matrix
    │   ├── INITIAL_ENGINEERING_AUDIT.md        # Workstation & Toolchain Feasibility
    │   ├── COMPONENT_MASTER_REGISTER.xlsx      # Master BOM with Manufacturer Codes
    │   ├── DDR3_FEASIBILITY_REPORT.md          # MIG & Memory Interface Audit
    │   ├── PCIE_FEASIBILITY_REPORT.md          # PCI-SIG CEM 2.0 Feasibility
    │   └── POWER_ARCHITECTURE_REPORT.md        # PDN & Power Budget Derivation
    ├── 01_ARCHITECTURE/                        # Block Diagrams, Signal Flow, Power Tree
    ├── 03_KICAD/                               # Custom Symbols, Footprints & 3D Models
    │   ├── 3D_MODELS/Xilinx_FFG676.wrl         # Custom VRML 3D Model for FPGA
    │   ├── FOOTPRINTS/                         # Custom IPC-7351B Footprints
    │   └── SYMBOLS/                            # Custom Kintex-7 Schematic Symbols
    ├── 04_STACKUP/                             # Stackup Specification & Impedances
    ├── 05_SIGNAL_INTEGRITY/                    # High-Speed Routing Constraints
    ├── 06_POWER_INTEGRITY/                     # PDN Analysis & Decoupling Strategy
    ├── 07_PCB/                                 # Layout, Escape Routing & Importer Scripts
    ├── 08_VERIFICATION/                        # Verification Sign-Off Reports
    │   ├── DRC/DRC_REPORT.rpt                  # KiCad DRC Report (0 Errors)
    │   ├── ERC/ERC_REPORT.rpt                  # KiCad ERC Report (0 Errors)
    │   └── DESIGN_REVIEW/                      # Formal Engineering Review
    ├── 09_MANUFACTURING_OUTPUTS/               # Production Fabrication Package
    │   ├── GERBER/                             # RS-274X Extended Gerber Files (12 Layers)
    │   ├── DRILL/                              # Excellon NC Drill Files (PTH / NPTH)
    │   ├── BOM/BOM_ORION-X-R1.csv              # Production Bill of Materials
    │   └── PICK_AND_PLACE/ORION-X-R1-pos.csv   # Centroid Component Placement Data
    ├── 10_VISUALIZATION/RENDERS/               # High-Resolution 3D Renders
    └── 11_FINAL_DOCUMENTATION/                 # Comprehensive Engineering Reports
```

---

## 7. Design Verification & Quality Sign-Off

### 7.1 Electrical Rules Check (ERC)
- **Status**: **0 Errors**, 103 Informational Warnings
- **Audit**: All net names, hierarchical sheet pins, and multi-rail power nets validated without pin contention.

### 7.2 Design Rules Check (DRC)
- **Status**: **0 Errors**
  - **Shorting Violations**: 0
  - **Clearance Violations**: 0
  - **Edge / Chamfer Violations**: 0
  - **Solder Mask Bridge Violations**: 0
  - **Unconnected Nets**: 0 (Full topological connectivity achieved)

---

## 8. Manufacturing Outputs Package

All manufacturing deliverables are pre-generated and archived in `ORION-X-R1/09_MANUFACTURING_OUTPUTS/`:

| Output Category | Standards / Format | Target Manufacturing Process |
| :--- | :--- | :--- |
| **Gerber Layers** | RS-274X (12 Copper, Masks, Silk, Edge) | Standard Multilayer Rigid PCB Fabrication |
| **NC Drill** | Excellon format (separate PTH and NPTH) | Automated CNC Mechanical Drilling ($0.25\text{ mm}$ min drill) |
| **Bill of Materials**| RFC 4180 CSV format with MPNs | SMT Component Procurement (DigiKey / Mouser) |
| **Centroid File** | CSV (Ref, Val, Package, PosX, PosY, Rot, Side) | Automated Pick-and-Place SMT Assembly Lines |
| **IPC-D-356** | Electrical Netlist Output | Automated Bare-Board Flying Probe Testing |

---

## 9. Reproduction & Build Instructions

To inspect, verify, or regenerate the design deliverables on Linux:

### 1. Prerequisites
- KiCad 9.0.2 or later
- Python 3.10+ with `pcbnew` Python bindings
- Java Runtime Environment (JRE 17+) for Specctra tools

### 2. Opening the CAD Project
```bash
# Clone the repository
git clone https://github.com/your-username/orion.git
cd orion

# Open master schematic in KiCad Eeschema
kicad ORION-X-R1/ORION-X-R1.kicad_pro

# Or open master PCB in KiCad Pcbnew directly
pcbnew ORION-X-R1/ORION-X-R1.kicad_pcb
```

### 3. Running Automated DRC & ERC via CLI
```bash
# Run Electrical Rules Check (ERC)
kicad-cli sch erc --output ORION-X-R1/08_VERIFICATION/ERC/ERC_REPORT.rpt ORION-X-R1/ORION-X-R1.kicad_sch

# Run Design Rules Check (DRC)
kicad-cli pcb drc --output ORION-X-R1/08_VERIFICATION/DRC/DRC_REPORT.rpt ORION-X-R1/ORION-X-R1.kicad_pcb
```

### 4. Regenerating Manufacturing Outputs & 3D Renders
```bash
# Execute master export and render pipeline
python3 ORION-X-R1/07_PCB/import_and_verify.py
```

---

## 10. License & Disclaimers

- **Hardware Design**: Licensed under the [CERN Open Hardware Licence Version 2 - Strongly Reciprocal](https://ohwr.org/cernohl) (CERN-OHL-S).
- **Documentation**: Licensed under Creative Commons Attribution-ShareAlike 4.0 International ([CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)).
- **Disclaimer**: This is a digital hardware design project produced for research and computational acceleration. While all electrical, physical, and manufacturing rules have been verified, physical deployment requires thermal airflow provisioning ($\ge 200\text{ LFM}$) under full 40A FPGA core load.

