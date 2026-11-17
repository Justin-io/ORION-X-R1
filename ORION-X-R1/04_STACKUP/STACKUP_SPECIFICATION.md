# 12-LAYER CONTROLLED-IMPEDANCE PCB STACKUP SPECIFICATION
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: STK-SPEC-001

---

### 1. PHYSICAL CONSTRUCTION & LAYER STACK TABLE

- **Total Finished Thickness**: $1.60\text{ mm} \pm 10\%$ ($63.0\text{ mil}$).
- **Material Base**: Isola FR408HR High-Tg ($T_g = 190^\circ\text{C}$, $T_d = 360^\circ\text{C}$, low loss).
- **Dielectric Constant ($D_k$)**: $3.65$ nominal at $2.5\text{ GHz} - 5.0\text{ GHz}$.
- **Loss Tangent ($D_f$)**: $0.0092$ at $5.0\text{ GHz}$.
- **Symmetry**: Fully symmetric construction around center core (L6–L7) to guarantee zero mechanical bow or twist.

| Layer Number | Layer Name | Layer Function | Copper Thickness | Dielectric Material | Dielectric Thickness | Dielectric Dk | Target Impedance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Top** | Top Silkscreen | Text & Component Outlines | N/A | White Liquid Photoimageable | N/A | N/A | N/A |
| **Top Mask** | Top Solder Mask | Solder Bridging Prevention | N/A | Taiyo PSR-4000 (Green) | 15.0 µm | 3.50 | N/A |
| **L1** | `F.Cu` | High-Speed Signal / Microstrip | 35.0 µm (1.0 oz) | N/A | N/A | N/A | $50\ \Omega$ SE, $85\ \Omega$ Diff (PCIe), $100\ \Omega$ Diff (DDR) |
| *D1-2* | Dielectric 1-2 | Prepreg Isolation | N/A | 2× 1080 / 2116 Prepreg | 100.0 µm | 3.65 | Return reference for L1 |
| **L2** | `In1.Cu` | Continuous Ground Plane | 17.5 µm (0.5 oz) | N/A | N/A | N/A | Solid RF Ground Reference |
| *D2-3* | Dielectric 2-3 | Core Isolation | N/A | FR408HR Laminate Core | 130.0 µm | 3.70 | Reference spacing |
| **L3** | `In2.Cu` | High-Speed Signal / Stripline | 17.5 µm (0.5 oz) | N/A | N/A | N/A | $50\ \Omega$ SE, $85\ \Omega$ Diff (PCIe), $100\ \Omega$ Diff (DDR) |
| *D3-4* | Dielectric 3-4 | Prepreg Isolation | N/A | 1× 2116 Prepreg | 130.0 µm | 3.65 | Reference spacing |
| **L4** | `In3.Cu` | Continuous Ground Plane | 17.5 µm (0.5 oz) | N/A | N/A | N/A | Solid RF Ground Reference |
| *D4-5* | Dielectric 4-5 | Core Isolation | N/A | FR408HR Laminate Core | 150.0 µm | 3.70 | Power/Ground isolation |
| **L5** | `In4.Cu` | Power Plane (VCCINT 1.00V) | 35.0 µm (1.0 oz) | N/A | N/A | N/A | Low-inductance 15A Core Plane |
| *D5-6* | Dielectric 5-6 | Prepreg Isolation | N/A | 1× 7628 Prepreg | 150.0 µm | 3.65 | Core inter-plane isolation |
| **L6** | `In5.Cu` | Continuous Ground Plane | 17.5 µm (0.5 oz) | N/A | N/A | N/A | Center Shield Ground Plane |
| *D6-7* | Dielectric 6-7 | Center Core Isolation | N/A | Heavy FR408HR Center Core | 200.0 µm | 3.75 | Center mechanical structural core |
| **L7** | `In6.Cu` | Continuous Ground Plane | 17.5 µm (0.5 oz) | N/A | N/A | N/A | Center Shield Ground Plane |
| *D7-8* | Dielectric 7-8 | Prepreg Isolation | N/A | 1× 7628 Prepreg | 150.0 µm | 3.65 | Core inter-plane isolation |
| **L8** | `In7.Cu` | Split Power Plane (VCCO/Aux) | 35.0 µm (1.0 oz) | N/A | N/A | N/A | VCCO_DDR (1.35V), VCCAUX (1.8V), 3.3V |
| *D8-9* | Dielectric 8-9 | Core Isolation | N/A | FR408HR Laminate Core | 150.0 µm | 3.70 | Power/Ground isolation |
| **L9** | `In8.Cu` | Continuous Ground Plane | 17.5 µm (0.5 oz) | N/A | N/A | N/A | Solid RF Ground Reference |
| *D9-10* | Dielectric 9-10 | Prepreg Isolation | N/A | 1× 2116 Prepreg | 130.0 µm | 3.65 | Reference spacing |
| **L10** | `In9.Cu` | High-Speed Signal / Stripline | 17.5 µm (0.5 oz) | N/A | N/A | N/A | $50\ \Omega$ SE, $100\ \Omega$ Diff (DDR Fly-by) |
| *D10-11*| Dielectric 10-11| Core Isolation | N/A | FR408HR Laminate Core | 130.0 µm | 3.70 | Reference spacing |
| **L11** | `In10.Cu` | Continuous Ground Plane | 17.5 µm (0.5 oz) | N/A | N/A | N/A | Solid RF Ground Reference |
| *D11-12*| Dielectric 11-12| Prepreg Isolation | N/A | 2× 1080 / 2116 Prepreg | 100.0 µm | 3.65 | Return reference for L12 |
| **L12** | `B.Cu` | Secondary Signal / Decoupling | 35.0 µm (1.0 oz) | N/A | N/A | N/A | $50\ \Omega$ SE, Local Power Islands |
| **Bot Mask** | Bottom Solder Mask | Solder Bridging Prevention | N/A | Taiyo PSR-4000 (Green) | 15.0 µm | 3.50 | N/A |
| **Bot Silk** | Bottom Silkscreen | Text & Test Identifiers | N/A | White Liquid Photoimageable | N/A | N/A | N/A |

**Total Dielectric Thickness**: $100 + 130 + 130 + 150 + 150 + 200 + 150 + 150 + 130 + 130 + 100 = 1470\ \mu\text{m}$ ($1.47\text{ mm}$).
**Total Copper Thickness**: $35 + 17.5 + 17.5 + 17.5 + 35 + 17.5 + 17.5 + 35 + 17.5 + 17.5 + 17.5 + 35 = 279\ \mu\text{m}$ ($0.279\text{ mm}$).
**Finished Board Thickness**: $1.470\text{ mm} + 0.279\text{ mm} = 1.60\text{ mm} \pm 10\%$.

