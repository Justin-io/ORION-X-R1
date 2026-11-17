# SUBSYSTEM INTERFACE MATRIX
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: ARCH-INT-001

---

| Source Subsystem | Destination Subsystem | Signal Group / Bus | Signal Count | Electrical Standard | Impedance Target | Max Data Rate / Freq | Isolation / Protection |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PCIe Edge (J1)** | FPGA Bank 115 (GTX) | `PCIE_TX[3:0]_P/N` | 8 nets (4 pairs) | CML Differential | $85\ \Omega$ Diff | 5.0 GT/s (Gen2) | 100 nF AC Caps (0402) |
| **PCIe Edge (J1)** | FPGA Bank 115 (GTX) | `PCIE_RX[3:0]_P/N` | 8 nets (4 pairs) | CML Differential | $85\ \Omega$ Diff | 5.0 GT/s (Gen2) | Direct DC (Host Motherboard Caps) |
| **PCIe Edge (J1)** | FPGA Bank 115 (GTX) | `PCIE_CLK_P/N` | 2 nets (1 pair) | HCSL Differential | $85\ \Omega$ Diff | 100.000 MHz | 100 nF AC Caps (0402) |
| **PCIe Edge (J1)** | FPGA Bank 14 (HR) | `PCIE_PERST#` | 1 net | 3.3V LVTTL | $50\ \Omega$ SE | DC / Asynch Reset | Schmitt-Trigger Buffer + 4.7k Pullup |
| **PCIe Edge (J1)** | FPGA Bank 14 (HR) | `PCIE_WAKE#` | 1 net | Open-Drain | $50\ \Omega$ SE | DC Sideband | 10k Pullup to 3.3Vaux |
| **FPGA Bank 32 (HP)** | DRAM U2 (Device 0) | `DDR_DQ[15:0]`, `DQS[1:0]`, `DM[1:0]` | 22 nets | SSTL135 | $50\ \Omega$ SE / $100\ \Omega$ Diff | 1600 MT/s (800 MHz) | On-Die Termination (ODT) |
| **FPGA Bank 34 (HP)** | DRAM U3 (Device 1) | `DDR_DQ[31:16]`, `DQS[3:2]`, `DM[3:2]` | 22 nets | SSTL135 | $50\ \Omega$ SE / $100\ \Omega$ Diff | 1600 MT/s (800 MHz) | On-Die Termination (ODT) |
| **FPGA Bank 33 (HP)** | DRAM U2 & U3 (Fly-by) | `DDR_A[14:0]`, `BA[2:0]`, Control | 25 nets | SSTL135 | $50\ \Omega$ SE | 800 MHz | $39.2\ \Omega$ Parallel Term to VTT |
| **FPGA Bank 33 (HP)** | DRAM U2 & U3 (Fly-by) | `DDR_CK_P/N` | 2 nets (1 pair) | DIFF_SSTL135 | $100\ \Omega$ Diff | 800 MHz | $100\ \Omega$ Diff Term at Bus End |
| **Oscillator (Y1)** | FPGA Bank 33 (MRCC) | `SYS_CLK_P/N` | 2 nets (1 pair) | LVDS Differential | $100\ \Omega$ Diff | 200.000 MHz | Internal $100\ \Omega$ FPGA Termination |
| **FPGA Bank 14 (HR)** | QSPI Flash (U4) | `SPI_CS#`, `CLK`, `D[3:0]` | 6 nets | 3.3V LVCMOS | $50\ \Omega$ SE | 66 MHz / 133 MHz | 4.7k Pullups on CS#/HOLD# |
| **JTAG Header (J2)** | FPGA Bank 0 (Config) | `TCK`, `TMS`, `TDI`, `TDO` | 4 nets | 3.3V LVCMOS | $50\ \Omega$ SE | Up to 30 MHz | 4.7k Pullup on TMS/TDI |
| **FPGA Bank 15 (HR)** | Management Header (J3) | `UART_TX`, `RX`, `I2C_SCL`, `SDA` | 4 nets | 3.3V LVCMOS | $50\ \Omega$ SE | 115,200 Baud / 400 kHz | ESD Protection Diode Array |
| **FPGA Bank 15 (HR)** | Status LEDs | `LED[7:0]` | 8 nets | 3.3V LVCMOS | N/A | Static / Blink | $330\ \Omega$ Current Limiting Resistors |
| **FPGA Bank 12 (HR)** | GPIO Header (J4) | `GPIO[15:0]` | 16 nets | 3.3V LVCMOS | $50\ \Omega$ SE | Up to 100 MHz | Damping Resistors / ESD Arrays |
