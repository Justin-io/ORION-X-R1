# MATERIAL ASSUMPTIONS & FABRICATION SPECIFICATION
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: MAT-SPEC-001

---

### 1. RAW MATERIAL SYSTEM

- **Laminate & Prepreg**: Isola FR408HR (High-Performance Multifunctional Epoxy).
  - Glass transition temperature: $T_g = 190^\circ\text{C}$ (DMA) / $175^\circ\text{C}$ (DSC).
  - Decomposition temperature: $T_d = 360^\circ\text{C}$ (TGA 5% weight loss).
  - Time to delamination: $T_{288} > 60\text{ minutes}$, $T_{300} > 15\text{ minutes}$.
  - CTE (Z-axis, $50^\circ\text{C} - 260^\circ\text{C}$): $2.8\%$.
  - Dielectric Constant ($D_k$): $3.65 \pm 0.05$ across $2\text{ GHz} - 10\text{ GHz}$.
  - Dissipation Factor ($\tan \delta$): $0.0092$ at $5\text{ GHz}$.
- **Copper Foil**: Electrodeposited Reverse-Treated Foil (RTF) or Very Low Profile (VLP) copper.
  - Outer foil base: 1.0 oz ($35\ \mu\text{m}$ nominal), plated up to ~45 µm in barrels.
  - Inner foil base: 0.5 oz ($17.5\ \mu\text{m}$ nominal) for signal/ground, 1.0 oz ($35\ \mu\text{m}$) for high-current power planes L5 and L8.
  - Copper surface roughness ($R_z$): $< 2.5\ \mu\text{m}$ (VLP class).
- **Solder Mask**: Taiyo PSR-4000 series (Green gloss, halogen-free, liquid photoimageable).
  - Nominal thickness over trace crown: $12 - 18\ \mu\text{m}$.
  - Dielectric constant: $3.50$ at $1\text{ MHz}$.
  - Dielectric strength: $> 500\text{ V/mil}$.

---

### 2. FABRICATION CAPABILITY ASSUMPTIONS (TIER-2 STANDARD HIGH-DENSITY INTERCONNECT)

- Minimum outer track width: $0.125\text{ mm}$ (5.0 mil).
- Minimum outer track clearance: $0.125\text{ mm}$ (5.0 mil).
- Minimum inner track width: $0.100\text{ mm}$ (3.9 mil).
- Minimum inner track clearance: $0.100\text{ mm}$ (3.9 mil).
- Minimum via drill diameter: $0.250\text{ mm}$ (9.8 mil mechanical CNC).
- Minimum via annular ring: $0.100\text{ mm}$ (4.0 mil) $\rightarrow$ Via pad diameter: $0.450\text{ mm}$ (17.7 mil).
- Board edge clearance: $0.350\text{ mm}$ (13.8 mil) to copper traces, $0.500\text{ mm}$ to plane copper.
- Aspect ratio (Board thickness / drill): $1.60\text{ mm} / 0.250\text{ mm} = 6.4:1$ (well within standard plating limits of $\le 10:1$).
- Surface finish: Electroless Nickel Immersion Gold (ENIG) — $3-5\ \mu\text{m}$ Ni, $0.05-0.1\ \mu\text{m}$ Au. Hard gold on PCIe edge fingers: $30\ \mu\text{in}$ ($0.76\ \mu\text{m}$) hard gold over $150\ \mu\text{in}$ ($3.8\ \mu\text{m}$) electrolytic nickel.

