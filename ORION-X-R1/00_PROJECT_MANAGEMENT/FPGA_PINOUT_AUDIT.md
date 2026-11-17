# FPGA PINOUT AUDIT & CLASSIFICATION REPORT
## Project: ORION-X R1.0
## Target Device: AMD Kintex-7 XC7K160T-2FFG676C

---

### 1. SUMMARY OF BALL CLASSIFICATION

| Category | Ball Count | Voltage Domain | Primary Functional Assignment |
| :--- | :--- | :--- | :--- |
| **CONFIG_JTAG_XADC** | 20 | 3.3V / 1.8V | Bank 0 Dedicated Configuration, JTAG, and Analog XADC |
| **GND** | 121 | 0.0V | System Ground Return Reference Matrix |
| **GTX_SIGNALS** | 40 | CML Differential | GTX Transceiver TX/RX/REFCLK (Bank 115 PCIe, Bank 116 Expansion) |
| **HP_IO_BANKS** | 150 | 1.35V (SSTL135) | Banks 32, 33, 34: 32-bit DDR3L Memory Interface & System Clock |
| **HR_IO_BANKS** | 250 | 3.3V (LVCMOS33) | Banks 12, 13, 14, 15, 16: QSPI Flash, PCIe Sidebands, UART, I2C, GPIO |
| **MGT_POWER** | 15 | 1.0V / 1.2V / 1.8V | GTX Transceiver Analog Supplies (MGTAVCC, MGTAVTT, MGTVCCAUX) |
| **VCCAUX** | 8 | 1.8V Nom (1.71V - 1.89V) | Auxiliary Circuits, CMT/PLLs, JTAG buffers |
| **VCCBRAM** | 4 | 1.0V Nom | Internal Block RAM Arrays |
| **VCCINT** | 16 | 1.0V Nom (0.97V - 1.03V) | Internal Core Logic Array |
| **VCCO** | 52 | Bank-Specific (1.35V / 3.3V) | I/O Bank Output Buffers (8 Banks) |
| **TOTAL** | **676** | | **100% of FFG676 Balls Accounted For** |

---

### 2. DETAILED BANK BREAKDOWN

| Bank ID | Type | I/O Count | VCCO Pins | Assigned Voltage | Assigned Subsystem Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bank 0** | Dedicated Config | 23 | N/A (VCCO_0 shared) | 3.3V (CFGBVS=VCCO_0) | JTAG, CCLK, PROGRAM_B, DONE, INIT_B, XADC |
| **Bank 12** | High-Range (HR) | 50 | 7 | 3.3V | General Purpose High-Speed Expansion Header (J4) |
| **Bank 13** | High-Range (HR) | 50 | 6 | 3.3V | Auxiliary GPIO & Board Test Points |
| **Bank 14** | High-Range (HR) | 50 | 6 | 3.3V | Quad-SPI Flash (FCS_B, D00..D03), PCIe PERST#, WAKE# |
| **Bank 15** | High-Range (HR) | 50 | 6 | 3.3V | Management UART, I2C Bus, Status LEDs, Reset Button |
| **Bank 16** | High-Range (HR) | 50 | 7 | 3.3V | Expansion & Logic Analyzer Mictor Header |
| **Bank 32** | High-Performance (HP) | 50 | 6 | 1.35V | DDR3L Device 0 Data (Byte 0: DQ[7:0], Byte 1: DQ[15:8]) |
| **Bank 33** | High-Performance (HP) | 50 | 6 | 1.35V | DDR3L Address A[14:0], BA[2:0], Control, CK/CK#, SYS_CLK |
| **Bank 34** | High-Performance (HP) | 50 | 6 | 1.35V | DDR3L Device 1 Data (Byte 2: DQ[23:16], Byte 3: DQ[31:24]) |
| **Bank 115** | GTX Transceiver | 8 pairs (4 ch) | N/A (MGT Rails) | CML (85 Ohm Diff) | PCI Express Gen2 x4 Transmit & Receive Lanes 0..3 |
| **Bank 116** | GTX Transceiver | 8 pairs (4 ch) | N/A (MGT Rails) | CML (100 Ohm Diff) | High-Speed Transceiver Expansion (SFP+ / SATA / Aurora) |

