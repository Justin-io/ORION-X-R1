# COMPONENT COMPATIBILITY & LIFECYCLE REPORT
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: CMP-RPT-001

---

### 1. COMPONENT LIFECYCLE & AVAILABILITY MATRIX

| Reference | Manufacturer Part Number (MPN) | Functional Description | Lifecycle Status | RoHS / REACH | Operating Temp Range | Target Interface | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | `XC7K160T-2FFG676C` | AMD Kintex-7 FPGA, 162K Logic Cells, 8 GTX | Active (Supported through 2035+) | RoHS-6 Compliant | 0°C to +85°C (Commercial) | PCIe Gen2, DDR3L, QSPI | **VERIFIED** |
| **U2** | `MT41K256M16TW-107-AAT:P` | Micron 4Gb DDR3L SDRAM x16 (TW Rev P) | Active | Lead-Free / RoHS Compliant | -40°C to +105°C (Auto) | DDR3L Lower 16-bit Bus | **VERIFIED** |
| **U3** | `MT41K256M16TW-107-AAT:P` | Micron 4Gb DDR3L SDRAM x16 (TW Rev P) | Active | Lead-Free / RoHS Compliant | -40°C to +105°C (Auto) | DDR3L Upper 16-bit Bus | **VERIFIED** |
| **U4** | `MX25L25645GMI-08G` | Macronix 256Mb Serial NOR Quad-SPI Flash | Active | Lead-Free / RoHS Compliant | -40°C to +85°C (Industrial) | FPGA Config Bank 14 / Bank 0 | **VERIFIED** |
| **U5** | `TPS546D24ARVFR` | TI 40A Synchronous Buck Converter with PMBus | Active | Lead-Free / Green (RoHS) | -40°C to +125°C (Tj) | FPGA VCCINT / VCCBRAM (1.0V) | **VERIFIED** |
| **U6** | `TPSM63610RDHR` | TI 10A Synchronous Buck Module w/ Inductor | Active | Lead-Free / Green (RoHS) | -40°C to +125°C (Tj) | DDR3L VDD/VDDQ (1.35V) | **VERIFIED** |
| **U7** | `TPSM63610RDHR` | TI 10A Synchronous Buck Module w/ Inductor | Active | Lead-Free / Green (RoHS) | -40°C to +125°C (Tj) | FPGA VCCAUX / MGTVCCAUX (1.8V) | **VERIFIED** |
| **U8** | `TPSM63610RDHR` | TI 10A Synchronous Buck Module w/ Inductor | Active | Lead-Free / Green (RoHS) | -40°C to +125°C (Tj) | System +3.3V Peripheral Rail | **VERIFIED** |
| **U9** | `TPS51200DRCR` | TI 3A Sinking/Sourcing DDR Termination LDO | Active | Lead-Free / Green (RoHS) | -40°C to +125°C (Tj) | DDR3 VTT (0.675V) & VREF | **VERIFIED** |
| **U10** | `TPS7A8500RTER` | TI 4A High-Accuracy Ultra-Low Noise LDO | Active | Lead-Free / Green (RoHS) | -40°C to +125°C (Tj) | GTX Transceiver MGTAVCC (1.0V) | **VERIFIED** |
| **U11** | `TPS7A8500RTER` | TI 4A High-Accuracy Ultra-Low Noise LDO | Active | Lead-Free / Green (RoHS) | -40°C to +125°C (Tj) | GTX Transceiver MGTAVTT (1.2V) | **VERIFIED** |
| **Y1** | `SiT9121AI-2B3-33E200.000000` | SiTime 200.000 MHz Differential LVDS XO | Active | Lead-Free / RoHS Compliant | -40°C to +85°C (Industrial) | FPGA Bank 33 MRCC (DDR3 MIG) | **VERIFIED** |
| **J1** | `PCIe-Edge-x4` | Standard PCI Express x4 Gold Finger Edge | Active / Standard | Hard Gold 30 µin over Ni | -40°C to +85°C | Host PCIe Slot Interface | **VERIFIED** |

---

### 2. SUBSYSTEM INTERFACE COMPATIBILITY AUDIT

#### 2.1 FPGA Core and Memory Voltage Matching
- **Constraint**: Kintex-7 High-Performance (HP) banks support supply voltages from 1.2V to 1.8V. High-Range (HR) banks support 1.2V to 3.3V.
- **Analysis**: The Micron `MT41K256M16TW-107-AAT:P` operates at $V_{DD} = V_{DDQ} = 1.35\text{V}$ (DDR3L mode). This voltage falls strictly within the allowable $V_{CCO}$ operating window of Kintex-7 HP banks (Banks 32, 33, 34). By setting $V_{CCO\_32} = V_{CCO\_33} = V_{CCO\_34} = 1.35\text{V}$, native SSTL135 electrical standards (`SSTL135` / `DIFF_SSTL135`) are directly synthesized by the FPGA I/O buffers without external level conversion.

#### 2.2 FPGA Configuration and SPI Flash Compatibility
- **Constraint**: The Macronix `MX25L25645GMI-08G` is a 3.3V NOR Flash device ($V_{CC} = 2.7\text{V} - 3.6\text{V}$). The Kintex-7 dedicated configuration pins (Bank 0) and multi-function pins (Bank 14) must operate at matching logic levels.
- **Analysis**: In the 7-Series architecture, setting pin `CFGBVS_0` (P7) to $V_{CCO\_0}$ allows Bank 0 to operate at 3.3V LVCMOS. Bank 14 is a High-Range (HR) bank and is powered from $+3.3\text{V\_SYS}$ ($V_{CCO\_14} = 3.3\text{V}$). All 4 SPI data lines (`MOSI/D00`, `DIN/D01`, `D02`, `D03`), chip select (`FCS_B`), and clock (`CCLK`) operate natively at 3.3V LVCMOS, achieving maximum Quad-SPI read rates (up to 66 MHz boot clock).

#### 2.3 PCI Express Gen2 x4 Physical Interface Matching
- **Constraint**: Host transmit differential pairs are AC coupled on the motherboard. The add-in card must provide AC coupling on its transmit pairs (`TX[3:0]`) while keeping its receive pairs (`RX[3:0]`) DC coupled.
- **Analysis**: Kintex-7 GTX transceivers incorporate internal programmable termination resistors (typically 100 $\Omega$ differential DC or AC coupled). Four 100 nF (0402, 16V, X7R) ceramic capacitors are incorporated on `PCIE_TX[3:0]_P/N` adjacent to the card edge fingers. Return paths are continuous to the underlying solid L2 ground plane.

#### 2.4 Power Distribution Sourcing & Thermal Verification
- **Constraint**: Total card power dissipation must remain within the standard PCIe x4 slot delivery capability ($25\text{W}$ initial allocation, expandable up to $66\text{W}$ via slot $+12\text{V}$ pins).
- **Analysis**:
  - Core logic (`VCCINT` 1.0V @ 8A typical, 12A peak) = 8.0W – 12.0W.
  - DDR3L memory (2 devices @ 1.35V, 1.8A aggregate) = 2.4W.
  - FPGA Aux & I/O (`VCCAUX` 1.8V @ 1.2A, `VCCO` 3.3V @ 0.8A) = 4.8W.
  - Transceivers (`MGTAVCC` 1.0V @ 1.2A, `MGTAVTT` 1.2V @ 1.0A) = 2.4W.
  - Regulators & losses (~10%) = 2.2W.
  - **Total Estimated Operating Power**: $19.8\text{W}$ typical, $23.8\text{W}$ maximum under heavy synthetic acceleration workload.
  - **Compliance**: Fully compliant with the 25W standard slot envelope; no auxiliary 6-pin PCIe power connector required.

---

### 3. CONCLUSION & APPROVAL

All proposed primary active and passive components are verified for electrical compatibility, lifecycle support, package availability, and interface voltage matching. The architecture is cleared for schematic implementation.

