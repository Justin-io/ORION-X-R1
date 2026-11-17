# ORION-X R1 — HARDWARE DESIGN LIMITATIONS & ENGINEERING TRADE-OFFS

## 1. Executive Summary
This document delineates the technical boundaries, architectural compromises, known electrical limitations, and recommended revision milestones for the ORION-X R1 FPGA computing and PCIe accelerator platform. All limitations documented herein are technically substantiated through manufacturer specifications, CAD validation, and signal/power integrity simulations.

---

## 2. Interface Limitations & Constraints

### 2.1 PCI Express Interface
- **Bus Speed & Generation**: Hardware architecture is targeted and verified for **PCI Express Gen2 (5.0 GT/s)**. While Kintex-7 -2 speed grade transceivers support Gen3 (8.0 GT/s) in specific architectures, the XC7K160T integrated PCIe hard IP core (`PCIE_2_1`) is architecturally capped at Gen2 x4 or Gen2 x8 per AMD UG476/PG054.
- **Link Width**: Implemented as **x4 link width** (20 Gb/s raw aggregate theoretical bandwidth, ~1.6 GB/s payload throughput after 8b/10b encoding and protocol overhead). Transceiver Quad 116 remains dedicated to high-speed expansion header J3.
- **Bifurcation**: Motherboard slot bifurcation is not required; the card functions as an endpoint device with an internal single-function physical layer.

### 2.2 DDR3L Memory Interface
- **Maximum Frequency**: Verified MIG operating frequency is **800 MHz (DDR3-1600)** at CL=11. While the Micron MT41K256M16TW-107 silicon can achieve 933 MHz (DDR3-1866), 800 MHz is enforced to guarantee robust timing margin without requiring complex DCI (Digitally Controlled Impedance) over-temperature calibration loops in standard -2 commercial grade silicon.
- **Fly-By Termination Power**: High bus activity creates up to 1.8W of static and dynamic dissipation across the parallel $39.2\,\Omega$ VTT termination resistor network. Thermal airflow across the termination bank is recommended during sustained burst writes.
- **Addressing Topology**: Single-rank dual-device architecture (32-bit combined width, 1GB total density). Memory expansion beyond 1GB requires upgrading to 8Gb discrete DRAM dies (e.g. MT41K512M16).

---

## 3. Power Distribution & Thermal Boundaries

### 3.1 Maximum Continuous Core Dissipation
- The TI TPS546D24ARVFR core buck converter provides up to **40A continuous** output at 1.00V (40W). Under normal high-density acceleration workloads, FPGA core power is estimated at 18W–25W.
- **Thermal Boundary**: At loads $> 25\text{W}$, forced convection airflow ($\ge 200\text{ LFM}$) and a low-profile active heatsink on the FFG676 package are mandatory to maintain FPGA junction temperature $T_J < 85^\circ\text{C}$.

### 3.2 Total Board Power Envelope
- Total power consumption from the host PCIe slot is budgeted at **45W nominal, 55W peak**.
- Power delivery is drawn exclusively from the PCIe $+12\text{V}$ rail ($5.5\text{A}$ rating = $66\text{W}$ max slot limit). The host $+3.3\text{V}$ PCIe rail is utilized solely for auxiliary standby sense circuitry to prevent back-powering host motherboards.

---

## 4. Fabrication & Physical Layer Constraints

### 4.1 PCB Manufacturing Class
- **Layer Count**: 12 copper layers ($1.6\text{ mm} \pm 10\%$ nominal finished thickness).
- **Minimum Trace Width / Spacing**: $0.090\text{ mm} / 0.090\text{ mm}$ ($3.5\text{ mil} / 3.5\text{ mil}$), classified as IPC-6012 Class 3 / High Density Interconnect (HDI) Tier 1.
- **Via Technology**: Through-hole mechanically drilled vias ($0.25\text{ mm}$ drill, $0.50\text{ mm}$ annular pad). No blind or buried laser microvias are utilized in R1.0, preserving broad fabrication vendor compatibility and low manufacturing cost.

### 4.2 Solder Mask & Reflow Profile
- Lead-free SAC305 assembly profile compliant with J-STD-020E.
- Peak reflow temperature: $245^\circ\text{C} - 250^\circ\text{C}$ for 30–45 seconds. Moisture Sensitivity Level (MSL) 3 rating requires 24-hour pre-bake at $125^\circ\text{C}$ if packages are exposed to ambient humidity $> 30\%$ prior to surface mount assembly.

---

## 5. Planned R2.0 Architectural Enhancements
1. Migration to UltraScale+ architecture (`Kintex UltraScale+ KU3P/KU5P`) for native PCIe Gen3/Gen4 x8 and DDR4-2400 support.
2. Introduction of 1-step laser microvias (HDI Type II) for reduced BGA fanout density.
3. Integration of QSFP28 100G optical networking cage for standalone network acceleration.

