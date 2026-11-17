# ORION-X R1 — FOOTPRINT AUDIT & VERIFICATION REPORT

## 1. Executive Summary
This document provides the formal audit and physical dimensional verification for all custom and standard footprint definitions used on the ORION-X R1 accelerator board. All footprints have been verified against manufacturer mechanical packaging drawings and IPC-7351B standards for Non-Solder-Mask Defined (NSMD) and Solder-Mask Defined (SMD) pads.

---

## 2. Component Footprint Verification Matrix

| RefDes | Manufacturer MPN | Package Designation | Footprint Library Reference | Pitch (mm) | Pad Count | Inspection Status | Notes & Standard Compliance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | AMD XC7K160T-2FFG676C | FFG676 (FCBGA-676) | `orion_footprints:BGA-676_27.0x27.0mm_Layout26x26_P1.0mm` | 1.00 | 676 | **VERIFIED** | IPC-7351B Class B NSMD; pad $\varnothing 0.45\text{ mm}$, mask $\varnothing 0.55\text{ mm}$. Interstitial dogbones $0.50\text{ mm}$ via pad / $0.25\text{ mm}$ drill. |
| **U2, U3** | Micron MT41K256M16TW-107:P | FBGA-96 (TW) | `orion_footprints:FBGA-96_9.0x14.0mm_Layout9x16_P0.8mm` | 0.80 | 96 | **VERIFIED** | JEDEC MO-207 compliant; pad $\varnothing 0.40\text{ mm}$, mask $\varnothing 0.50\text{ mm}$. Dogbones $0.40\text{ mm}$ via pad / $0.20\text{ mm}$ drill. |
| **U4** | Macronix MX25L25645GMI-08G | 16-SOP (300 mil) | `Package_SO:SOIC-16W_7.5x10.3mm_P1.27mm` | 1.27 | 16 | **VERIFIED** | IPC-7351B SOIC127P1030X265-16N. Quad-SPI configuration memory. |
| **U5** | TI TPS546D24ARVFR | QFN-40 (RVF) | `orion_footprints:TI_RVF40_5x7mm_P0.5mm` | 0.50 | 40+EP | **VERIFIED** | Dual exposed ground/power pads with $4\times 3$ thermal via array for 40A dissipation. |
| **U6, U7, U8** | TI TPSM63610RDHR | QFN-29 (RDH) | `orion_footprints:TI_RDH29_5.0x5.5mm_P0.5mm` | 0.50 | 29+EP | **VERIFIED** | Integrated inductor power module footprint. Exposed thermal pads partitioned with solder mask dams. |
| **U9** | TI TPS51200DRCR | VSON-10 (DRC) | `Package_SON:VSON-10-1EP_3x3mm_P0.5mm_EP1.65x2.4mm` | 0.50 | 10+EP | **VERIFIED** | JEDEC MO-229; Exposed PowerPAD connected to solid ground with $2\times 2$ thermal via matrix. |
| **U10, U11**| TI TPS7A8500RTER | WQFN-20 (RTE) | `Package_DFN_QFN:WQFN-20-1EP_3.5x3.5mm_P0.5mm_EP2.1x2.1mm` | 0.50 | 20+EP | **VERIFIED** | Thermal pad with 4 ground vias for low thermal resistance $\theta_{JA} < 35.4^\circ\text{C/W}$. |
| **U12** | SiTime SiT9121AI-2B3-33E200 | SMD-6 (5032) | `Oscillator:Oscillator_SMD_SiTime_SiT8008_5.0x3.2mm` | 1.27 | 6 | **VERIFIED** | Standard 6-pin differential oscillator footprint with NC / Output Enable pins. |
| **J1** | PCI-SIG Card Edge | PCIe Gen2 x4 Edge | `orion_footprints:PCIe_x4_Edge_Connector` | 1.00 | 64 | **VERIFIED** | PCI Express Card Electromechanical Spec 2.0; Chamfered $20^\circ$ bevel edge, key slot at pos 11/12. |
| **J2** | Multicomp MC-254-14 | Shrouded Header 2x7 | `Connector_PinHeader_2.00mm:PinHeader_2x07_P2.00mm_Vertical` | 2.00 | 14 | **VERIFIED** | Standard AMD Xilinx 14-pin JTAG pinout with keyed shroud. |
| **J3** | Samtec QSH-030-01-L-D-A | High-Speed Socket 60 | `orion_footprints:Samtec_QSH-030-01-L-D-A` | 0.50 | 60+GND | **VERIFIED** | 0.5mm pitch high-speed differential board-to-board connector with integral central ground plane. |
| **L1** | Wurth 744314110 / Coilcraft | Inductor 10x10mm | `Inductor_SMD:L_10.2x10.2mm_H4.0mm` | - | 2 | **VERIFIED** | Low-DCR ($0.8\text{ m}\Omega$) high-saturation 45A power inductor. |

---

## 3. PCB Fabrication & Assembly Rules Compliance
1. **Solder Mask Clearance**: Standard $0.05\text{ mm}$ clearance around copper pads.
2. **Solder Mask Dam**: Minimum $0.075\text{ mm}$ web between adjacent QFN pins prevents bridging during automated reflow.
3. **Thermal Via Tent Strategy**: All thermal vias under exposed pads are tented on the bottom layer or plugged/capped to prevent solder wicking.

