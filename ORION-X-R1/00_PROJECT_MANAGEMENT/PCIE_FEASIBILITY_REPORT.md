# PCI EXPRESS GEN2 x4 HARDWARE INTERFACE FEASIBILITY REPORT
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: PCIE-RPT-001

---

### 1. INTERFACE SPECIFICATION & ARCHITECTURE

The ORION-X R1 accelerator interfaces directly with the host PC system via a 4-lane PCI Express Gen2 (5.0 GT/s) edge connector.

- **Standard**: PCI Express Base Specification Revision 2.1 / PCI Express Card Electromechanical (CEM) Specification 2.0.
- **Form Factor**: PCI Express Standard-Height Add-in Card (Half-Length, 4-Lane Physical Edge).
- **Link Bandwidth**:
  - Raw bit rate: 5.0 Gbps per lane.
  - 4 lanes aggregate: 20.0 Gbps.
  - Effective throughput (8b/10b encoding): 16.0 Gbps ($2.0\text{ GB/s}$ simplex, $4.0\text{ GB/s}$ duplex).
- **FPGA Hard IP Core**: AMD Kintex-7 Integrated Block for PCI Express (`PCIE_2_1` at location `PCIE_X0Y0`), which provides full physical, data link, and transaction layer compliance with zero programmable logic fabric overhead.

---

### 2. TRANSCEIVER ALLOCATION & PIN MAPPING (UG476 / PG054)

The `PCIE_X0Y0` primitive in the `XC7K160T-2FFG676C` is physically tied to the Gigabit Transceiver Quad 115 (Bank 115). All 4 differential TX and RX lanes are mapped strictly to Bank 115 channels:

| PCIe Channel | Signal Name | FPGA Ball Coordinate | Package Pin Name | KiCad Schematic Net | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Lane 0 TX** | `PCIE_TX0_P` / `N` | `P2` / `P1` | `MGTXTXP0_115` / `N0_115` | `PCIE_TX0_P` / `N` | Transmit Diff Pair (AC coupled to edge) |
| **Lane 0 RX** | `PCIE_RX0_P` / `N` | `R4` / `R3` | `MGTXRXP0_115` / `N0_115` | `PCIE_RX0_P` / `N` | Receive Diff Pair (DC coupled to edge) |
| **Lane 1 TX** | `PCIE_TX1_P` / `N` | `M2` / `M1` | `MGTXTXP1_115` / `N1_115` | `PCIE_TX1_P` / `N` | Transmit Diff Pair (AC coupled to edge) |
| **Lane 1 RX** | `PCIE_RX1_P` / `N` | `N4` / `N3` | `MGTXRXP1_115` / `N1_115` | `PCIE_RX1_P` / `N` | Receive Diff Pair (DC coupled to edge) |
| **Lane 2 TX** | `PCIE_TX2_P` / `N` | `K2` / `K1` | `MGTXTXP2_115` / `N2_115` | `PCIE_TX2_P` / `N` | Transmit Diff Pair (AC coupled to edge) |
| **Lane 2 RX** | `PCIE_RX2_P` / `N` | `L4` / `L3` | `MGTXRXP2_115` / `N2_115` | `PCIE_RX2_P` / `N` | Receive Diff Pair (DC coupled to edge) |
| **Lane 3 TX** | `PCIE_TX3_P` / `N` | `H2` / `H1` | `MGTXTXP3_115` / `N3_115` | `PCIE_TX3_P` / `N` | Transmit Diff Pair (AC coupled to edge) |
| **Lane 3 RX** | `PCIE_RX3_P` / `N` | `J4` / `J3` | `MGTXRXP3_115` / `N3_115` | `PCIE_RX3_P` / `N` | Receive Diff Pair (DC coupled to edge) |
| **Host REFCLK**| `PCIE_CLK_P` / `N` | `H6` / `H5` | `MGTREFCLK0P_115` / `N0_115` | `PCIE_CLK_P` / `N` | 100 MHz HCSL Host Differential Clock |
| **GTX Calib** | `MGTRREF_115` | `M6` | `MGTRREF_115` | `MGTRREF` | Calibration Resistor ($100\ \Omega \pm 1\%$ to GND) |

---

### 3. TRANSMISSION LINE CONSTRAINTS & STACKUP MATCHING

- **Differential Target Impedance**: $Z_{\text{diff}} = 85\ \Omega \pm 10\%$ (recommended for PCIe Gen2/Gen3 to minimize return loss and reflection against connector/package discontinuities; $100\ \Omega$ is also permissible, but $85\ \Omega$ is optimal per PCI-SIG guidelines).
- **Single-Ended Impedance**: $Z_0 = 50\ \Omega \pm 10\%$.
- **Layer Allocation**:
  - `PCIE_TX[3:0]` and `PCIE_RX[3:0]` routed as edge-coupled microstrip on Layer 1 (Top) and Layer 3 (Inner Stripline).
  - Continuous reference to Layer 2 Ground.
- **Trace Geometry (calculated for 85-ohm differential microstrip on L1)**:
  - Trace width $W = 0.14\text{ mm}$ (5.5 mil).
  - Trace spacing $S = 0.15\text{ mm}$ (6.0 mil).
  - Dielectric height to L2 Ground $H = 0.10\text{ mm}$ (4.0 mil, Isola FR408HR $\varepsilon_r = 3.65$).
- **Intra-Pair Skew Constraint**: Length mismatch between P and N traces within any differential pair must not exceed $0.12\text{ mm}$ ($\approx 0.8\text{ ps}$).
- **Inter-Lane Skew Constraint**: PCIe protocol incorporates internal elastic elastic buffers and lane deskew logic supporting up to $20\text{ ns}$ of inter-lane skew. Physical trace lengths across lanes are matched within $5.0\text{ mm}$ for optimal signal integrity.

---

### 4. AC COUPLING & RETURN PATH DISCONTINUITIES

- **Capacitor Selection**: Murata `GCM155R71C104KA55D` (0.1 µF / 100 nF, 16V, X7R, 0402 package).
- **Placement**: Located immediately adjacent to the edge connector pads on the top and bottom layers.
- **Voiding under Pads**: To prevent capacitive impedance dips at the 0402 solder pads, the reference Ground plane on L2 is voided directly beneath the capacitor solder pads with the solid reference picked up on L3.
- **Via Transitions**: Transceiver signals transitioning between L1 and L3 have adjacent ground return vias placed within $0.5\text{ mm}$ of the signal via barrel to maintain unbroken RF ground return current loops.

---

### 5. EDGE CONNECTOR PINOUT & POWER ENTRY

- **PCIe Sideband Signals**:
  - `PERST#` (Pin A11): Active-low fundamental reset from host motherboard. Routed to FPGA Bank 14 (3.3V HR Bank) via schmitt-trigger buffer and $4.7\text{ k}\Omega$ pull-up to $+3.3\text{V\_SYS}$.
  - `WAKE#` (Pin B11): Open-drain wake signal to motherboard.
  - `PRSNT1#` (Pin A1) and `PRSNT2#` (Pin B17 for x4): Connected together on the card to indicate physical presence of an x4 card to the motherboard power management circuitry.
- **Card Power Delivery**:
  - Motherboard $+12\text{V}$ pins (B1, B2, B3, A2, A3) provide up to 5.5A ($66\text{W}$). This is the primary input to the onboard switching buck regulators (`TPS546D24A` and `TPSM63610`).
  - Motherboard $+3.3\text{V}$ pins (B10, B11, A9, A10) provide auxiliary logic power.

---

### 6. CONCLUSION

The PCI Express Gen2 x4 interface architecture conforms completely with PCI-SIG CEM 2.0 and AMD Xilinx Kintex-7 guidelines. Physical routing constraints and component selections are verified.

