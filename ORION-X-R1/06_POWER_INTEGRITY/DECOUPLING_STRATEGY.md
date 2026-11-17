# ORION-X R1 — DECOUPLING AND BYPASSING STRATEGY

## 1. Scope & Standards
This document defines the physical placement, capacitor selection, loop-inductance optimization, and layout rules for the decoupling capacitor network on the ORION-X R1 accelerator board, adhering to:
- **AMD Xilinx UG483**: *7 Series FPGAs PCB Design Guide*
- **Micron TN-41-01**: *DDR3 Design Guide & Power Decoupling*
- **PCI-SIG CEM 2.0**: *PCI Express Card Electromechanical Specification*

---

## 2. Decoupling Allocation Schedule

### 2.1 Kintex-7 XC7K160T-2FFG676C Decoupling Matrix

| Power Rail | Nominal Voltage | Required Bulk ($47\,\mu\text{F} - 100\,\mu\text{F}$) | Mid-Range ($4.7\,\mu\text{F} - 10\,\mu\text{F}$) | High-Frequency ($0.1\,\mu\text{F} - 1\,\mu\text{F}$) | Placement Zone |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **VCCINT** | 1.00 V | 2× 100 $\mu$F (1210) | 6× 10 $\mu$F (0805) | 16× 0.1 $\mu$F (0402) | B.Cu directly under BGA cavity & perimeter |
| **VCCAUX** | 1.80 V | 1× 47 $\mu$F (1206) | 4× 4.7 $\mu$F (0603) | 8× 0.1 $\mu$F (0402) | Adjacent to VCCAUX pin clusters |
| **VCCO_DDR** (Banks 32, 33, 34) | 1.35 V | 2× 47 $\mu$F (1206) | 6× 10 $\mu$F (0805) | 12× 0.1 $\mu$F (0402) | Under DRAM I/O banks on B.Cu |
| **VCCO_SYS** (Banks 0, 14, 15) | 3.30 V | 1× 22 $\mu$F (0805) | 3× 4.7 $\mu$F (0603) | 6× 0.1 $\mu$F (0402) | Perimeter near HR bank balls |
| **MGTAVCC** | 1.00 V | 1× 22 $\mu$F (0805) | 2× 4.7 $\mu$F (0603) | 4× 0.1 $\mu$F (0402) | Direct escape to Quad 115/116 transceiver balls |
| **MGTAVTT** | 1.20 V | 1× 22 $\mu$F (0805) | 2× 4.7 $\mu$F (0603) | 4× 0.1 $\mu$F (0402) | Direct escape to Quad 115/116 termination balls |

### 2.2 Micron DDR3L SDRAM (2× MT41K256M16TW-107) Decoupling Matrix

| Device | Rail | Bulk / Local | Per-Pin High-Frequency | Placement |
| :--- | :--- | :--- | :--- | :--- |
| **U2 (DRAM 0)** | VDD (1.35V) | 1× 10 $\mu$F (0805) | 4× 0.1 $\mu$F (0402) | B.Cu directly opposing BGA power balls |
| **U2 (DRAM 0)** | VDDQ (1.35V) | 1× 10 $\mu$F (0805) | 6× 0.1 $\mu$F (0402) | Reverse side of memory FBGA96 footprint |
| **U3 (DRAM 1)** | VDD (1.35V) | 1× 10 $\mu$F (0805) | 4× 0.1 $\mu$F (0402) | B.Cu directly opposing BGA power balls |
| **U3 (DRAM 1)** | VDDQ (1.35V) | 1× 10 $\mu$F (0805) | 6× 0.1 $\mu$F (0402) | Reverse side of memory FBGA96 footprint |
| **U9 (TPS51200)** | VTT_DDR | 1× 22 $\mu$F (0805) | 4× 0.1 $\mu$F (0402) | Distributed along address termination arrays |
| **U9 (TPS51200)** | VREF_DDR | 1× 1.0 $\mu$F (0603) | 2× 0.1 $\mu$F (0402) | At DRAM VREFCA / VREFDQ pins |

---

## 3. High-Frequency Decoupling Layout Rules

To ensure effective bypassing at frequencies exceeding 50 MHz, layout geometry must minimize loop inductance ($L_{loop}$):

1. **Direct Via-to-Pad Geometry**:
   - Every 0402 capacitor pad must connect immediately to its via with a short, wide trace ($W \ge 0.30\text{ mm}$, length $< 0.50\text{ mm}$).
   - Never daisy-chain multiple capacitor terminals across a single surface trace.
2. **Via Proximity and Mutual Inductance Cancellation**:
   - Power and Ground vias must be placed as close together as possible ($0.65\text{ mm}$ pitch) to leverage mutual inductive cancellation ($L_{net} = L_1 + L_2 - 2M$).
3. **Plane Drop Proximity**:
   - Decoupling capacitor GND vias connect directly to Layer 2 and Layer 4 ground planes with thermal-relief-less solid connections to minimize DC and AC impedance.
4. **Dielectric Cavity Advantage**:
   - B.Cu (Layer 12) capacitor placement couples directly into L11 (GND) and L8/L5 power planes with via lengths $< 0.6\text{ mm}$, providing substantially lower total inductance than surface components on F.Cu.

