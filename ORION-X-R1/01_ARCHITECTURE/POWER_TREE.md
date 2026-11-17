# COMPLETE POWER TREE SPECIFICATION
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: ARCH-PWR-001

---

### 1. POWER TREE SOURCING & CONVERSION TOPOLOGY

```mermaid
flowchart TD
    PCIE_12V["PCIe Edge +12V Bus (5.5A Max, 66W)"] --> U5_BUCK["U5: TPS546D24A (Synch Buck 40A)<br/>Efficiency: 91.5% @ 10A"]
    PCIE_12V --> U6_BUCK["U6: TPSM63610 (Module 10A)<br/>Efficiency: 89.8% @ 3A"]
    PCIE_12V --> U7_BUCK["U7: TPSM63610 (Module 10A)<br/>Efficiency: 90.5% @ 2A"]
    PCIE_12V --> U8_BUCK["U8: TPSM63610 (Module 10A)<br/>Efficiency: 93.0% @ 2A"]

    U5_BUCK -->|Stage 1: PGOOD1| VCCINT["VCCINT (1.00V @ 12A pk)<br/>FPGA Core Logic"]
    U5_BUCK --> VCCBRAM["VCCBRAM (1.00V @ 1.5A)<br/>FPGA Block RAM"]

    U7_BUCK -->|Stage 2: PGOOD2| VCCAUX["VCCAUX (1.80V @ 2.5A pk)<br/>FPGA CMT/PLL & JTAG"]
    U7_BUCK --> MGTVCCAUX["MGTVCCAUX (1.80V @ 0.4A)<br/>GTX Quad PLLs (LC Filtered)"]
    U7_BUCK --> U11_LDO["U11: TPS7A8500 (LDO 4A)<br/>PSRR > 55dB @ 500kHz"]

    U6_BUCK -->|Stage 3: PGOOD3| VCCO_DDR["VCCO_DDR (1.35V @ 4A pk)<br/>Banks 32, 33, 34 & Micron DRAM"]
    U6_BUCK --> U9_LDO["U9: TPS51200 (Term LDO 3A)<br/>Tracking VDDQ/2"]
    U6_BUCK --> U10_LDO["U10: TPS7A8500 (LDO 4A)<br/>PSRR > 55dB @ 500kHz"]

    U8_BUCK -->|Stage 3: PGOOD3| VCC3V3_SYS["+3.3V_SYS (3.30V @ 2.5A)<br/>Banks 0, 12, 13, 14, 15, 16 & Flash"]

    U9_LDO -->|Stage 4| VTT_DDR["VTT_DDR (0.675V ± 2A pk)<br/>Fly-by Bus Termination"]
    U9_LDO --> VREF_DDR["VREF_DDR (0.675V @ 10mA)<br/>DRAM & FPGA Reference"]

    U10_LDO --> MGTAVCC["MGTAVCC (1.00V @ 1.8A pk)<br/>GTX Transceiver Core (<10mVpp)"]
    U11_LDO --> MGTAVTT["MGTAVTT (1.20V @ 1.5A pk)<br/>GTX Termination (<10mVpp)"]
```

---

### 2. POWER TREE PARAMETRIC SUMMARY TABLE

| Rail Name | Input Rail | Regulator IC | Topology | Nominal Voltage | Tolerance | Max Current | Output Power | Ripple Target |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **+12V_PCIE** | Host Slot | Edge Connector | Direct | 12.0 V | $\pm 8\%$ | 3.5 A (typ) | 42.0 W | $\pm 100\text{ mV}$ |
| **VCCINT** | +12V_PCIE | `U5: TPS546D24A` | Buck (PMBus) | 1.00 V | $\pm 3\%$ | 12.0 A (pk) | 12.0 W | $< 10\text{ mV}_{\text{p-p}}$ |
| **VCCBRAM** | +12V_PCIE | `U5: TPS546D24A` | Buck | 1.00 V | $\pm 3\%$ | 1.5 A | 1.5 W | $< 10\text{ mV}_{\text{p-p}}$ |
| **VCCO_DDR** | +12V_PCIE | `U6: TPSM63610` | Buck Module | 1.35 V | $\pm 5\%$ | 4.0 A (pk) | 5.4 W | $< 15\text{ mV}_{\text{p-p}}$ |
| **VCCAUX** | +12V_PCIE | `U7: TPSM63610` | Buck Module | 1.80 V | $\pm 5\%$ | 2.5 A (pk) | 4.5 W | $< 15\text{ mV}_{\text{p-p}}$ |
| **+3.3V_SYS** | +12V_PCIE | `U8: TPSM63610` | Buck Module | 3.30 V | $\pm 5\%$ | 2.5 A (pk) | 8.25 W | $< 25\text{ mV}_{\text{p-p}}$ |
| **VTT_DDR** | VCCO_DDR | `U9: TPS51200` | Sink/Source LDO | 0.675 V | $\pm 3\%$ | $\pm 2.0\text{ A}$ | 1.35 W | $< 10\text{ mV}_{\text{p-p}}$ |
| **MGTAVCC** | VCCO_DDR | `U10: TPS7A8500` | Ultra-Low Noise | 1.00 V | $\pm 3\%$ | 1.8 A | 1.8 W | $< 10\text{ mV}_{\text{p-p}}$ |
| **MGTAVTT** | VCCAUX | `U11: TPS7A8500` | Ultra-Low Noise | 1.20 V | $\pm 3\%$ | 1.5 A | 1.8 W | $< 10\text{ mV}_{\text{p-p}}$ |
| **MGTVCCAUX**| VCCAUX | LC Filter Island | Passive Filter | 1.80 V | $\pm 5\%$ | 0.4 A | 0.72 W | $< 5\text{ mV}_{\text{p-p}}$ |

