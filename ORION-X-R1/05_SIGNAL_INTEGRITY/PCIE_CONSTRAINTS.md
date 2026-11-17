# PCI EXPRESS GEN2 x4 ROUTING CONSTRAINTS & GUIDELINES
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: SI-PCIE-001

---

### 1. NETCLASS DEFINITIONS & GEOMETRIES

```
NetClass "PCIE_TX":
  - Net names: PCIE_TX0_P, PCIE_TX0_N, PCIE_TX1_P, PCIE_TX1_N, PCIE_TX2_P, PCIE_TX2_N, PCIE_TX3_P, PCIE_TX3_N
  - Layer: Layer 1 (Top Microstrip)
  - Trace Width (W): 0.180 mm (7.1 mil)
  - Differential Pair Gap (S): 0.125 mm (4.9 mil)
  - Target Differential Impedance: 85.0 Ohm +/- 10%
  - Target Single-Ended Impedance: 52.0 Ohm +/- 10%
  - Trace Clearance to Unrelated Copper: >= 0.500 mm (>= 3W spacing)

NetClass "PCIE_RX":
  - Net names: PCIE_RX0_P, PCIE_RX0_N, PCIE_RX1_P, PCIE_RX1_N, PCIE_RX2_P, PCIE_RX2_N, PCIE_RX3_P, PCIE_RX3_N
  - Layer: Layer 3 (Inner Stripline between L2 GND and L4 GND)
  - Trace Width (W): 0.100 mm (3.9 mil)
  - Differential Pair Gap (S): 0.170 mm (6.7 mil)
  - Target Differential Impedance: 85.0 Ohm +/- 10%
  - Target Single-Ended Impedance: 48.0 Ohm +/- 10%
  - Trace Clearance to Unrelated Copper: >= 0.400 mm

NetClass "PCIE_REFCLK":
  - Net names: PCIE_CLK_P, PCIE_CLK_N
  - Layer: Layer 1 (Top Microstrip)
  - Trace Width (W): 0.180 mm
  - Differential Pair Gap (S): 0.125 mm
  - Target Differential Impedance: 85.0 Ohm +/- 10%
```

---

### 2. LENGTH MATCHING & SKEW BUDGETS

- **Intra-Pair Skew (P to N within any differential pair)**:
  - Max allowable skew: $\pm 0.8\text{ ps}$.
  - Equivalent PCB trace length mismatch: $\le 0.12\text{ mm}$ ($\le 5.0\text{ mil}$).
  - Tuning method: Phase-matching bump / trombone placed immediately adjacent to any uncoupled section or bend.
- **Inter-Lane Skew (Lane to Lane)**:
  - Maximum protocol allowable skew: $20.0\text{ ns}$ (handled by PCIe PHY elastic buffer).
  - Target layout matching: all 4 lanes matched within $\pm 2.50\text{ mm}$ ($\pm 16\text{ ps}$) to minimize buffer latency.

---

### 3. VIA TRANSITIONS & RETURN PATH RULES

1. **Ground Return Vias**: Where differential pairs transition between L1 and L3, two ground stitching vias must be placed symmetrically on both sides of the differential pair within $0.50\text{ mm}$ of the signal via pads.
2. **Layer Transitions**: Maximum of 2 via transitions per differential channel (1 breakout via at FPGA BGA, 1 arrival via at edge connector / capacitor).
3. **No Split Planes**: Differential traces must never cross splits or voids in their reference planes (L2 and L4).

