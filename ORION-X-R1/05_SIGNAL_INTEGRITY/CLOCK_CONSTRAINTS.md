# CLOCK SYSTEM DISTRIBUTION & INTEGRITY CONSTRAINTS
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: SI-CLK-001

---

### 1. CLOCK ARCHITECTURE & ROUTING RULES

| Clock Signal | Frequency | Electrical Standard | Source | Destination | Target Zdiff | Max Skew | Routing Layer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PCIE_CLK_P/N** | 100.000 MHz | HCSL Differential | PCIe Host Edge (J1) | FPGA Bank 115 `MGTREFCLK0` | $85.0\ \Omega \pm 10\%$ | $\pm 0.8\text{ ps}$ | L1 Microstrip |
| **SYS_CLK_P/N** | 200.000 MHz | LVDS Differential | SiTime Oscillator (Y1) | FPGA Bank 33 `MRCC` (`AB11/AC11`) | $100.0\ \Omega \pm 10\%$ | $\pm 1.0\text{ ps}$ | L3 Stripline |
| **DDR_CK_P/N** | 800.000 MHz | DIFF_SSTL135 | FPGA Bank 33 `DQS` (`AB12/AC12`) | DRAM U2 & U3 Clock Inputs | $100.0\ \Omega \pm 10\%$ | $\pm 1.0\text{ ps}$ | L10 Stripline |
| **FPGA_CCLK** | Up to 66 MHz | 3.3V LVCMOS | FPGA Bank 0 Dedicated | QSPI Flash SCLK (U4) | $50.0\ \Omega \pm 10\%$ | N/A | L1 Microstrip |

---

### 2. CLOCK ISOLATION & JITTER MITIGATION

1. **Guard Traces / Spacing**: All differential clock pairs must maintain a minimum physical clearance of $4W$ ($0.50\text{ mm}$ to $0.80\text{ mm}$) to any adjacent switching data bus, power rail, or clock trace.
2. **Reference Continuity**: Clocks routed on L1 reference solid L2 Ground. Clocks routed on L3 reference solid L2 and L4 Ground. Clocks routed on L10 reference solid L9 and L11 Ground.
3. **Power Supply Filtering**: Oscillator `Y1` 3.3V supply is isolated via an SMD ferrite bead (Murata BLM18PG121SN1D, $120\ \Omega$ @ 100MHz) and decoupled with a parallel combination of $10\ \mu\text{F}$ (0603) and $0.1\ \mu\text{F}$ (0402) ceramic capacitors.

