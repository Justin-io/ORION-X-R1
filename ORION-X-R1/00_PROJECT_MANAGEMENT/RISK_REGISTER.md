# PROJECT RISK REGISTER
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: RSK-REG-001

---

| Risk ID | Risk Category | Description of Risk Event | Initial Severity | Probability | Engineered Mitigation Action | Residual Severity | Residual Probability | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-001** | High-Speed Layout | DDR3L timing violation due to PCB propagation delay mismatch on byte lanes or fly-by bus. | HIGH | HIGH | Strict serpentine length-tuning rules configured in KiCad netclasses: $\pm 0.75\text{ mm}$ intra-byte, $\pm 0.15\text{ mm}$ intra-pair skew, fly-by delay compensation via 7-Series MIG write leveling. | LOW | LOW | **MITIGATED** |
| **RSK-002** | Power Integrity | Excessive $V_{\text{CCINT}}$ dynamic ripple during high-current accelerator burst transitions causing FPGA logic soft errors. | CRITICAL | MEDIUM | Deployed 40A PMBus buck converter (`TPS546D24A`) with low-ESR ceramic decoupling array (37 capacitors total) and solid power plane on L5 immediately adjacent to L4/L6 ground planes. | LOW | LOW | **MITIGATED** |
| **RSK-003** | Signal Integrity | GTX Transceiver phase jitter degradation due to switching noise from onboard DC-DC converters. | HIGH | MEDIUM | Dedicated ultra-low-noise linear LDOs (`TPS7A8500`) powering MGTAVCC (1.0V) and MGTAVTT (1.2V) with $<10\ \mu\text{V}_{\text{RMS}}$ noise and localized ferrite bead filtering. | LOW | LOW | **MITIGATED** |
| **RSK-004** | Thermal Management | FPGA junction temperature exceeding $85^\circ\text{C}$ under heavy computational load ($15\text{W}$ dissipation). | HIGH | MEDIUM | Standard 4-hole heatsink mounting pattern (58.5 mm pitch) incorporated around FFG676 package with bottom-layer thermal copper pour and inner plane thermal conduction vias. | MEDIUM | LOW | **MANAGED** |
| **RSK-005** | BGA Manufacturability | Solder bridging or open circuits during BGA assembly on 1.0mm pitch 676-ball package. | HIGH | LOW | Standard through-hole dogbone fanout with $0.45\text{ mm}$ pad / $0.25\text{ mm}$ drill vias, standard $0.53\text{ mm}$ NSMD pads, and $0.10\text{ mm}$ solder mask dam. Digital DRC fully verified. | LOW | LOW | **MITIGATED** |
| **RSK-006** | Configuration / Boot | QSPI Flash boot failure due to FPGA Bank 0/14 voltage incompatibility. | HIGH | LOW | Hardwired `CFGBVS_0` to `VCCO_0` (3.3V) and powered Bank 14 at 3.3V, natively matching the Macronix 3.3V NOR Flash logic levels. | LOW | LOW | **MITIGATED** |
| **RSK-007** | PCIe CEM Compliance | Card edge finger damage or impedance discontinuity on host motherboard insertion. | MEDIUM | MEDIUM | Enforced $85\ \Omega$ differential microstrip geometry, $20^\circ$ edge chamfer, and specified 30 µin hard gold plating over 150 µin electrolytic nickel. | LOW | LOW | **MITIGATED** |
| **RSK-008** | Power Sequencing | FPGA latch-up or damaged I/O buffers resulting from out-of-order power rail ramp. | CRITICAL | LOW | Hardware PGOOD cascade ladder strictly enforcing $V_{\text{CCINT}} \rightarrow V_{\text{CCAUX}} \rightarrow V_{\text{CCO}} \rightarrow V_{\text{TT}}$. | LOW | LOW | **MITIGATED** |

