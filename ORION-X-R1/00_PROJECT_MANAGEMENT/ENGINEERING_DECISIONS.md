# FORMAL ENGINEERING DECISION RECORD (EDR)
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: EDR-LOG-001

---

### EDR-001: Selection of FPGA Package and Family
- **Context**: High-density FPGA accelerator design requiring PCIe Gen2 x4 hard block, 32-bit DDR3L memory bus, and multiple high-speed serial transceivers.
- **Options Considered**:
  1. Artix-7 (XC7A200T): Lower cost, but restricted transceiver performance and limited HP banks.
  2. Kintex-7 (XC7K160T-2FFG676C): 162,240 logic cells, 8 GTX transceivers (up to 12.5 Gbps), 3 HP banks (150 pins) and 5 HR banks (250 pins), hard PCIe Gen2 IP.
  3. Virtex-7 (XC7VX330T): Excessively large package (FFG1157), significantly higher cost and power.
- **Decision**: Selected **AMD Xilinx XC7K160T-2FFG676C**.
- **Justification**: Meets all PCIe Gen2 x4 and 32-bit DDR3L bandwidth targets with optimal balance of logic density, transceiver speed grade (-2), and thermal performance in a standard 27x27 mm package.

---

### EDR-002: 32-bit DDR3L Bank and Topology Architecture
- **Context**: 32-bit DDR3 memory interface requires 4 data byte groups plus address, command, and control lines.
- **Options Considered**:
  1. 2-Bank Mixed Layout: Cramming address/control and data into 2 banks. Violates Kintex-7 MIG byte lane routing rules and causes excessive cross-talk.
  2. 3-Bank Centered Layout: Center bank (Bank 33) dedicated to Address/Command/Control and System Clock; lower bank (Bank 32) dedicated to Device 0 Data (Bytes 0, 1); upper bank (Bank 34) dedicated to Device 1 Data (Bytes 2, 3).
- **Decision**: Selected **3-Bank Centered Layout (Bank 32, 33, 34)** with Fly-By topology.
- **Justification**: Conforms to AMD UG586 guidelines, guarantees lowest clock-to-address skew, provides symmetric routing to both DRAM devices, and enables 800 MHz DDR3-1600 operation.

---

### EDR-003: Core Voltage Regulator Topology (VCCINT)
- **Context**: FPGA core logic consumes up to 12A–15A dynamic current at 1.0V with tight $\pm 3\%$ transient tolerance.
- **Options Considered**:
  1. Traditional multi-phase controller with external discrete MOSFETs and driver ICs.
  2. Integrated power module (e.g. TPSM846C24).
  3. Single-IC 40A Synchronous Buck Converter with PMBus telemetry (`TPS546D24ARVFR`).
- **Decision**: Selected **TI `TPS546D24ARVFR`** with Coilcraft `XGL6060-331MEB` inductor.
- **Justification**: Compact 5x7 mm footprint, integrated high-efficiency NexFETs, PMBus 1.3 monitoring of core current/voltage/temperature, >91% efficiency, and programmable transient loop response.

---

### EDR-004: GTX Transceiver Power Supply Filtering (MGTAVCC / MGTAVTT)
- **Context**: GTX transceivers require ultra-clean supplies ($<10\text{ mV}_{\text{p-p}}$ total noise) to prevent phase jitter and bit errors on PCIe links.
- **Options Considered**:
  1. Direct switching buck rail with ferrite bead filter. Risk of high-frequency ripple feedthrough.
  2. Linear ultra-low-noise LDOs (`TPS7A8500RTER`) fed from pre-regulated switching rails.
- **Decision**: Selected **Linear Ultra-Low-Noise LDOs (`TPS7A8500RTER`)**.
- **Justification**: Provides $>55\text{ dB}$ PSRR at the switching frequency, $<4.4\ \mu\text{V}_{\text{RMS}}$ noise floor, and guaranteed compliance with AMD Kintex-7 transceiver jitter specifications.

---

### EDR-005: PCB Stackup and Layer Count Determination
- **Context**: BGA escape routing under 676-ball 1.0mm package, 32-bit DDR3 routing, PCIe differential routing, and low-impedance power planes.
- **Options Considered**:
  1. 8-layer stackup: Severe routing congestion, compromised ground return paths, split power planes under high-speed traces.
  2. 10-layer stackup: Marginally feasible, but lacks dedicated power plane separation for VCCINT and VCCO.
  3. 12-layer symmetric stackup: 6 signal layers, 4 continuous ground planes, 2 dedicated power planes.
- **Decision**: Selected **12-Layer Symmetric Stackup (1.60 mm finished thickness)**.
- **Justification**: Provides uninterrupted stripline and microstrip ground references for all high-speed signals, isolates sensitive MGT transceivers, and maintains mechanical symmetry to prevent board warpage during reflow.

