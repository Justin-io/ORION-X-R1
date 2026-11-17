# DDR3L-1600 ROUTING CONSTRAINTS & TIMING BUDGET
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: SI-DDR3-001

---

### 1. NETCLASS DEFINITIONS & IMPEDANCE SPECIFICATION

```
NetClass "DDR_DQ":
  - Net names: DDR_DQ[31:0], DDR_DM[3:0]
  - Layers: Layer 1 (Byte 0/1 Top Microstrip), Layer 3 (Byte 2/3 Inner Stripline)
  - Trace Width (L1): 0.190 mm (50 Ohm SE)
  - Trace Width (L3): 0.120 mm (50 Ohm SE)
  - Clearance: >= 2W (0.380 mm on L1, 0.250 mm on L3)

NetClass "DDR_DQS":
  - Net names: DDR_DQS0_P/N, DDR_DQS1_P/N, DDR_DQS2_P/N, DDR_DQS3_P/N
  - Layers: Layer 1 (Byte 0/1 Microstrip), Layer 3 (Byte 2/3 Stripline)
  - Target Differential Impedance: 100.0 Ohm +/- 10%
  - Geometry (L1): W = 0.135 mm, S = 0.160 mm
  - Geometry (L3): W = 0.100 mm, S = 0.240 mm

NetClass "DDR_CLK":
  - Net names: DDR_CK_P, DDR_CK_N
  - Layer: Layer 10 (Inner Stripline between L9 GND and L11 GND)
  - Target Differential Impedance: 100.0 Ohm +/- 10%
  - Geometry (L10): W = 0.100 mm, S = 0.240 mm

NetClass "DDR_ADDR":
  - Net names: DDR_A[14:0], DDR_BA[2:0], DDR_RAS#, DDR_CAS#, DDR_WE#, DDR_CS#, DDR_CKE, DDR_ODT
  - Layer: Layer 10 (Inner Stripline)
  - Target Single-Ended Impedance: 50.0 Ohm +/- 10%
  - Geometry (L10): W = 0.120 mm
```

---

### 2. LENGTH & SKEW MATCHING MATRIX

```
+---------------------------------------------------------------------------------+
| Byte Lane 0: DDR_DQ[7:0], DDR_DM0 to DDR_DQS0_P/N                              |
|   - Max Skew: +/- 5 ps (+/- 0.75 mm)                                            |
|   - Reference: DDR_DQS0_P/N length                                              |
|                                                                                 |
| Byte Lane 1: DDR_DQ[15:8], DDR_DM1 to DDR_DQS1_P/N                             |
|   - Max Skew: +/- 5 ps (+/- 0.75 mm)                                            |
|   - Reference: DDR_DQS1_P/N length                                              |
|                                                                                 |
| Byte Lane 2: DDR_DQ[23:16], DDR_DM2 to DDR_DQS2_P/N                            |
|   - Max Skew: +/- 5 ps (+/- 0.75 mm)                                            |
|   - Reference: DDR_DQS2_P/N length                                              |
|                                                                                 |
| Byte Lane 3: DDR_DQ[31:24], DDR_DM3 to DDR_DQS3_P/N                            |
|   - Max Skew: +/- 5 ps (+/- 0.75 mm)                                            |
|   - Reference: DDR_DQS3_P/N length                                              |
|                                                                                 |
| Address/Command/Control: DDR_A[14:0], BA[2:0], CTRL to DDR_CK_P/N               |
|   - Max Skew: +/- 25 ps (+/- 3.75 mm)                                           |
|   - Reference: DDR_CK_P/N length                                                |
|                                                                                 |
| Differential Pairs: DDR_DQS[3:0]_P to N, DDR_CK_P to N                          |
|   - Max Intra-Pair Skew: +/- 1.0 ps (+/- 0.15 mm)                               |
+---------------------------------------------------------------------------------+
```

---

### 3. FLY-BY ROUTING ORDER & TERMINATION

1. Signals exit FPGA Bank 33 on Layer 10 (Stripline).
2. Traces route first to Device 0 (`U2: MT41K256M16`), dropping vias to BGA pads.
3. Traces continue uninterrupted on Layer 10 to Device 1 (`U3: MT41K256M16`).
4. Past Device 1, traces transition to Layer 1 / Layer 12 through-vias and connect directly to $39.2\ \Omega \pm 1\%$ surface-mount resistor arrays tied to the $V_{\text{TT\_DDR}}$ power copper plane.
5. Stub length from the main fly-by trunk to any DRAM ball pad must not exceed $1.20\text{ mm}$ ($47\text{ mil}$).
