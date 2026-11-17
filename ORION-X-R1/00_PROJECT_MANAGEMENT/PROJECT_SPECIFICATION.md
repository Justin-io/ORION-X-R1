# PROJECT SPECIFICATION: ORION-X R1
## High-Density FPGA Computing & PCIe Accelerator Platform
## Document ID: SPEC-ORION-001
## Revision: 1.0

---

### 1. SYSTEM SPECIFICATIONS

| Parameter | Specification | Verification Method |
| :--- | :--- | :--- |
| **Project Identity** | ORION-X Revision 1.0 (ORION-X-R1) | Project Master Directory |
| **Primary FPGA Device** | AMD Kintex-7 `XC7K160T-2FFG676C` | Official AMD Pinout Audit |
| **Logic Cell Density** | 162,240 Logic Cells (25,350 Slices, 101,400 CLB flip-flops) | AMD DS182 Data Sheet |
| **Block RAM** | 11,700 Kb (325 Blocks × 36 Kb) | AMD DS182 Data Sheet |
| **DSP Slices** | 600 DSP48E1 Slices | AMD DS182 Data Sheet |
| **Transceivers** | 8× GTX Transceivers (supporting up to 12.5 Gbps) | AMD UG476 Specification |
| **Host Interface** | PCI Express Gen2 x4 (5.0 GT/s per lane, 2.0 GB/s throughput) | AMD PG054 / PCI-SIG CEM 2.0 |
| **External Memory** | 8Gb (1GB) DDR3L-1600 (32-bit bus, 2× 256M×16 Micron DRAM) | AMD UG586 / JEDEC JESD79-3 |
| **Memory Bandwidth** | 6.4 GB/s peak theoretical bandwidth at 800 MHz clock | Timing Budget Calculation |
| **Configuration Flash** | 256Mb (32MB) Serial NOR Quad-SPI Flash (`MX25L25645GMI-08G`) | AMD UG470 Specification |
| **System Clock** | 200.000 MHz LVDS Low-Jitter Oscillator (`SiT9121`, < 500 fs RMS) | SiTime Datasheet Specification |
| **Board Form Factor** | PCIe Standard-Height Add-in Card (Length: 167.65 mm, Height: 111.15 mm) | PCI-SIG CEM 2.0 Mechanical |
| **PCB Layer Count** | 12 Copper Layers (Symmetric construction, 1.60 mm finished) | 12-Layer Stackup Calculation |
| **Controlled Impedance** | $50\ \Omega$ Single-Ended, $100\ \Omega$ Diff (DDR3/Clock), $85\ \Omega$ Diff (PCIe) | 2D Field Solver Calculations |
| **Power Input** | +12V (up to 5.5A) and +3.3V (up to 3.0A) from PCIe Edge Connector | Power Budget Analysis |
| **Total Card Dissipation**| 19.8W typical, 23.8W maximum continuous | PDN Thermal Calculation |

---

### 2. SUBSYSTEM FUNCTIONAL ALLOCATION

- **Subsystem A (PCIe Edge)**: 4 Transmit pairs, 4 Receive pairs, 100MHz HCSL Clock, `PERST#`, `WAKE#`, `PRSNT#`, +12V & +3.3V power fingers.
- **Subsystem B (FPGA Core)**: Full XC7K160T-2FFG676C device, power/ground decoupling matrix, XADC analog monitoring, bank power filtering.
- **Subsystem C (DDR3L Memory)**: Two Micron MT41K256M16TW devices, 32-bit DQ bus, 4 DQS differential pairs, 4 DM lines, fly-by Address/Control, $V_{TT}$ termination network.
- **Subsystem D (Configuration)**: Macronix 256Mb Quad-SPI Flash, standard 14-pin JTAG header, boot mode selection pins (`M[2:0] = 001` for Master SPI x4), status LEDs (`DONE`, `INIT_B`).
- **Subsystem E (Clocking)**: 100 MHz PCIe host clock, 200 MHz local differential system oscillator, clock distribution and conditioning.
- **Subsystem F (Power Distribution)**: TI `TPS546D24A` (1.0V VCCINT @ 15A), TI `TPSM63610` (1.35V VCCO_DDR @ 4A), TI `TPSM63610` (1.8V VCCAUX @ 2.5A), TI `TPSM63610` (+3.3V_SYS @ 2.5A), TI `TPS51200` (VTT/VREF @ ±2A), TI `TPS7A8500` (MGTAVCC 1.0V & MGTAVTT 1.2V), PGOOD sequencing ladder.
- **Subsystem G (Management & Expansion)**: UART-to-host interface, I2C temperature/voltage telemetry bus, 8 user status LEDs, 20-pin GPIO expansion header, reset pushbutton.

