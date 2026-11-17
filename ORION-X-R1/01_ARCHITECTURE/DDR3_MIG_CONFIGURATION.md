# AMD MEMORY INTERFACE GENERATOR (MIG) CONFIGURATION REPORT
## Project: ORION-X R1.0
## Target Architecture: AMD 7-Series MIG (Vivado MIG 7-Series Core)
## Device: XC7K160T-2FFG676C
## Document ID: MIG-CFG-001

---

### 1. CONTROLLER ARCHITECTURE & CONFIGURATION PARAMETERS

The memory controller is configured using the AMD Vivado Memory Interface Generator (MIG 7-Series) targeting the Kintex-7 High-Performance (HP) banks.

| MIG Configuration Field | Parameter Value | Engineering Justification |
| :--- | :--- | :--- |
| **Memory Device Type** | `DDR3_SDRAM` (DDR3L Mode) | Backward-compatible low voltage ($1.35\text{V}$) operation. |
| **Memory Part Selected** | `MT41K256M16XX-107` (Custom Part Equivalent) | Micron 4Gb ($256\text{M}\times 16$), -107 timing grade. |
| **Data Width** | `32-Bit` ($2\times \text{x}16$ Devices) | 4 Byte Lanes: Byte 0/1 on Bank 32, Byte 2/3 on Bank 34. |
| **Memory Clock Period** | `1250 ps` ($800.000\text{ MHz}$) | DDR3-1600 timing specification (1600 MT/s). |
| **Controller Clock Ratio** | `4:1` | Controller UI clock operates at $200.000\text{ MHz}$. |
| **PHY / Memory Voltage** | `1.35V` (SSTL135) | High-Performance I/O banks operating at $V_{\text{CCO}} = 1.35\text{V}$. |
| **Internal VREF** | Enabled / External VREF Pins | High-accuracy reference supplied from `TPS51200` REFOUT ($0.675\text{V}$). |
| **Input Clock Period** | `5000 ps` ($200.000\text{ MHz}$) | Driven by onboard low-jitter differential oscillator `Y1: SiT9121`. |
| **Input Clock Type** | `Differential` (LVDS) | Directly feeds Bank 33 Multi-Region Clock Capable (`MRCC`) pins `AB11/AC11`. |
| **Output Driver Impedance** | `RZQ/7` ($34\ \Omega$) | Optimizes eye margin when terminated with $39.2\ \Omega$ to $V_{\text{TT}}$. |
| **On-Die Termination (ODT)** | `RZQ/4` ($60\ \Omega$) | High-frequency signal integrity on bi-directional data bus. |
| **Ordering** | `Normal` (Strict AXI4 Compliance) | Maintains deterministic memory transaction sequences. |

---

### 2. ADDRESS, COMMAND, CONTROL & CLOCK PIN ASSIGNMENT MATRIX

```
Bank 33: Address/Command/Control & Clock Bank (VCCO = 1.35V)
-----------------------------------------------------------
Signal Name         FPGA Pin   Pin Function           DRAM Pin   Termination
DDR_A[0]            AA8        IO_L10P_T1_33          N3 (A0)    39.2 Ohm to VTT
DDR_A[1]            AB7        IO_L7P_T1_33           P7 (A1)    39.2 Ohm to VTT
DDR_A[2]            AC7        IO_L7N_T1_33           P3 (A2)    39.2 Ohm to VTT
DDR_A[3]            AD6        IO_L8P_T1_33           N2 (A3)    39.2 Ohm to VTT
DDR_A[4]            AE7        IO_L8N_T1_33           P8 (A4)    39.2 Ohm to VTT
DDR_A[5]            AF7        IO_L5P_T0_33           P2 (A5)    39.2 Ohm to VTT
DDR_A[6]            AF8        IO_L5N_T0_33           R8 (A6)    39.2 Ohm to VTT
DDR_A[7]            AE8        IO_L6P_T0_33           R2 (A7)    39.2 Ohm to VTT
DDR_A[8]            AF9        IO_L6N_T0_33           T8 (A8)    39.2 Ohm to VTT
DDR_A[9]            AD10       IO_L16P_T2_33          R3 (A9)    39.2 Ohm to VTT
DDR_A[10]           AE10       IO_L16N_T2_33          L7 (A10)   39.2 Ohm to VTT
DDR_A[11]           AF10       IO_L17P_T2_33          R7 (A11)   39.2 Ohm to VTT
DDR_A[12]           AE11       IO_L17N_T2_33          N7 (A12)   39.2 Ohm to VTT
DDR_A[13]           AF11       IO_L18P_T2_33          T3 (A13)   39.2 Ohm to VTT
DDR_A[14]           AE13       IO_L20P_T3_33          T7 (A14)   39.2 Ohm to VTT
DDR_BA[0]           AA7        IO_L10N_T1_33          M2 (BA0)   39.2 Ohm to VTT
DDR_BA[1]           Y7         IO_L1N_T0_33           N8 (BA1)   39.2 Ohm to VTT
DDR_BA[2]           Y8         IO_L1P_T0_33           M3 (BA2)   39.2 Ohm to VTT
DDR_RAS#            AC13       IO_L19P_T3_33          J3 (RAS#)  39.2 Ohm to VTT
DDR_CAS#            AD13       IO_L19N_T3_33          K3 (CAS#)  39.2 Ohm to VTT
DDR_WE#             AA12       IO_L14P_T2_SRCC_33     L3 (WE#)   39.2 Ohm to VTT
DDR_CS#             AA13       IO_L14N_T2_SRCC_33     L2 (CS#)   39.2 Ohm to VTT
DDR_CKE             Y10        IO_L2P_T0_33           K9 (CKE)   39.2 Ohm to VTT
DDR_ODT             Y11        IO_L2N_T0_33           K1 (ODT)   39.2 Ohm to VTT
DDR_RESET#          W11        IO_L4P_T0_33           T2 (RESET#) 4.7k Pullup / VTT
DDR_CK_P            AB12       IO_L15P_T2_DQS_33      J7 (CK)    100 Ohm Diff Term
DDR_CK_N            AC12       IO_L15N_T2_DQS_33      K7 (CK#)   100 Ohm Diff Term
SYS_CLK_P           AB11       IO_L13P_T2_MRCC_33     From Y1    100 Ohm Internal
SYS_CLK_N           AC11       IO_L13N_T2_MRCC_33     From Y1    100 Ohm Internal
```

---

### 3. DATA BYTE LANE PIN ASSIGNMENT MATRIX

```
Bank 32: Device 0 Data Bank (Lower 16-Bit: Bytes 0 and 1)
---------------------------------------------------------
Signal Name         FPGA Pin   Byte Group   Pin Function         DRAM Pin
DDR_DQ[0]           AD15       T0           IO_L2P_T0_32         E3 (DQL0)
DDR_DQ[1]           AE15       T0           IO_L2N_T0_32         F7 (DQL1)
DDR_DQ[2]           AF14       T0           IO_L4P_T0_32         F2 (DQL2)
DDR_DQ[3]           AF15       T0           IO_L4N_T0_32         F8 (DQL3)
DDR_DQ[4]           AD16       T0           IO_L1P_T0_32         H3 (DQL4)
DDR_DQ[5]           AE16       T0           IO_L1N_T0_32         H8 (DQL5)
DDR_DQ[6]           AF17       T0           IO_L5P_T0_32         G2 (DQL6)
DDR_DQ[7]           AE17       T0           IO_L5N_T0_32         H7 (DQL7)
DDR_DQS0_P          AE18       T0           IO_L3P_T0_DQS_32     F3 (DQSL)
DDR_DQS0_N          AF18       T0           IO_L3N_T0_DQS_32     G3 (DQSL#)
DDR_DM0             AD17       T0           IO_L6P_T0_32         E7 (DML)

DDR_DQ[8]           AB14       T1           IO_L7P_T1_32         D7 (DQU0)
DDR_DQ[9]           AB15       T1           IO_L7N_T1_32         C3 (DQU1)
DDR_DQ[10]          AC14       T1           IO_L8P_T1_32         C8 (DQU2)
DDR_DQ[11]          AD14       T1           IO_L8N_T1_32         C2 (DQU3)
DDR_DQ[12]          AA14       T1           IO_L10P_T1_32        A7 (DQU4)
DDR_DQ[13]          AA15       T1           IO_L10N_T1_32        A2 (DQU5)
DDR_DQ[14]          W14        T1           IO_L11P_T1_SRCC_32   B8 (DQU6)
DDR_DQ[15]          W15        T1           IO_L11N_T1_SRCC_32   A3 (DQU7)
DDR_DQS1_P          Y15        T1           IO_L9P_T1_DQS_32     C7 (DQSU)
DDR_DQS1_N          Y16        T1           IO_L9N_T1_DQS_32     B7 (DQSU#)
DDR_DM1             W16        T1           IO_L12P_T1_MRCC_32   B3 (DMU)

Bank 34: Device 1 Data Bank (Upper 16-Bit: Bytes 2 and 3)
---------------------------------------------------------
Signal Name         FPGA Pin   Byte Group   Pin Function         DRAM Pin
DDR_DQ[16]          U1         T0           IO_L1P_T0_34         E3 (DQL0)
DDR_DQ[17]          V1         T0           IO_L1N_T0_34         F7 (DQL1)
DDR_DQ[18]          U2         T0           IO_L2P_T0_34         F2 (DQL2)
DDR_DQ[19]          V2         T0           IO_L2N_T0_34         F8 (DQL3)
DDR_DQ[20]          W3         T0           IO_L4P_T0_34         H3 (DQL4)
DDR_DQ[21]          Y3         T0           IO_L4N_T0_34         H8 (DQL5)
DDR_DQ[22]          Y1         T0           IO_L5P_T0_34         G2 (DQL6)
DDR_DQ[23]          Y2         T0           IO_L5N_T0_34         H7 (DQL7)
DDR_DQS2_P          W6         T0           IO_L3P_T0_DQS_34     F3 (DQSL)
DDR_DQS2_N          W5         T0           IO_L3N_T0_DQS_34     G3 (DQSL#)
DDR_DM2             V4         T0           IO_L6P_T0_34         E7 (DML)

DDR_DQ[24]          AA2        T1           IO_L12N_T1_MRCC_34   D7 (DQU0)
DDR_DQ[25]          AA3        T1           IO_L12P_T1_MRCC_34   C3 (DQU1)
DDR_DQ[26]          AC2        T1           IO_L11N_T1_SRCC_34   C8 (DQU2)
DDR_DQ[27]          AB2        T1           IO_L11P_T1_SRCC_34   C2 (DQU3)
DDR_DQ[28]          AD1        T1           IO_L10N_T1_34        A7 (DQU4)
DDR_DQ[29]          AE1        T1           IO_L10P_T1_34        A2 (DQU5)
DDR_DQ[30]          AF2        T1           IO_L8N_T1_34         B8 (DQU6)
DDR_DQ[31]          AF3        T1           IO_L8P_T1_34         A3 (DQU7)
DDR_DQS3_P          AB1        T1           IO_L9P_T1_DQS_34     C7 (DQSU)
DDR_DQS3_N          AC1        T1           IO_L9N_T1_DQS_34     B7 (DQSU#)
DDR_DM3             AE3        T1           IO_L7P_T1_34         B3 (DMU)
```

---

### 4. SUMMARY

The memory pin assignment completely obeys AMD 7-Series MIG byte group placement rules:
1. Every DQ line resides in the same byte group as its corresponding DQS pair and DM line.
2. Differential strobes (`DQS_P/N`) are placed exclusively on dedicated `IO_L..._DQS` pins.
3. System reference clock (`SYS_CLK_P/N`) is placed on Bank 33 `MRCC` clock-capable pins.
4. Memory differential clock (`DDR_CK_P/N`) is placed on Bank 33 dedicated `DQS` differential clock pins.
5. All address and control lines are localized to Bank 33, maintaining short, symmetric fly-by traces to both DRAM devices.

