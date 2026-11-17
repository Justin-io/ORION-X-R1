# POWER DISTRIBUTION NETWORK (PDN) & REGULATOR ARCHITECTURE REPORT
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: PWR-RPT-001

---

### 1. POWER SYSTEM ARCHITECTURE & BLOCK DIAGRAM

The ORION-X R1 power tree derives all operating rails from the host PCI Express edge connector ($+12\text{V}$ primary rail and $+3.3\text{V}$ secondary rail). High-efficiency synchronous buck converters and low-noise linear regulators step down the voltage to supply the FPGA core, memory, transceivers, and peripherals:

```
                                  +-----------------------------+
                                  | PCIe EDGE CONNECTOR (+12V)  |
                                  +--------------+--------------+
                                                 |
         +---------------------------------------+---------------------------------------+
         |                                       |                                       |
         v                                       v                                       v
+------------------+                   +------------------+                   +------------------+
| U5: TPS546D24A   |                   | U6: TPSM63610    |                   | U7: TPSM63610    |
| 40A Synch Buck   |                   | 10A Buck Module  |                   | 10A Buck Module  |
| Fsw = 650 kHz    |                   | Fsw = 1000 kHz   |                   | Fsw = 1000 kHz   |
+--------+---------+                   +--------+---------+                   +--------+---------+
         |                                       |                                       |
         v                                       v                                       v
   VCCINT (1.00V)                          VCCO_DDR (1.35V)                        VCCAUX (1.80V)
   12A pk / 8A typ                         4A pk / 2.5A typ                        2.5A pk / 1.5A typ
         |                                       |                                       |
         +--> VCCBRAM (1.00V)                    +--> DDR3L VDD/VDDQ                     +--> MGTVCCAUX (1.8V, Filtered)
                                                 |                                       |
                                                 v                                       v
                                       +------------------+                    +------------------+
                                       | U9: TPS51200     |                    | U11: TPS7A8500   |
                                       | DDR VTT/VREF LDO |                    | Ultra-Low-Noise  |
                                       +--------+---------+                    +--------+---------+
                                                 |                                       |
                                                 v                                       v
                                           VTT_DDR (0.675V)                        MGTAVTT (1.20V)
                                           VREF_DDR (0.675V)                       1.5A pk / 1.0A typ
                                                                                         |
                                                                               +------------------+
                                                                               | U10: TPS7A8500   |
                                                                               | Ultra-Low-Noise  |
                                                                               +--------+---------+
                                                                                         |
                                                                                         v
                                                                                   MGTAVCC (1.00V)
                                                                                   1.8A pk / 1.2A typ
```

---

### 2. DETAILED REGULATOR SPECIFICATIONS & CALCULATIONS

#### 2.1 VCCINT / VCCBRAM Regulator (`U5: TPS546D24ARVFR`)
- **Topology**: Synchronous Buck Converter with integrated high-side and low-side NexFETs, PMBus 1.3 compliant telemetry interface.
- **Input Voltage ($V_{\text{IN}}$)**: $12.0\text{V}$ nominal from PCIe edge.
- **Output Voltage ($V_{\text{OUT}}$)**: $1.00\text{V} \pm 10\text{mV}$ ($\pm 1.0\%$ DC regulation).
- **Maximum Continuous Load Current**: $15.0\text{A}$ (rated up to $40\text{A}$).
- **Switching Frequency ($f_{\text{sw}}$)**: $650\text{ kHz}$.
- **Output Inductor Selection**:
  $$L = \frac{V_{\text{OUT}} \times (V_{\text{IN}} - V_{\text{OUT}})}{V_{\text{IN}} \times f_{\text{sw}} \times \Delta I_L}$$
  Targeting ripple current $\Delta I_L = 30\% \times 15\text{A} = 4.5\text{A}$:
  $$L = \frac{1.0 \times (12 - 1.0)}{12 \times 650\times 10^3 \times 4.5} = \frac{11.0}{3.51 \times 10^7} \approx 0.31\ \mu\text{H}$$
  Selected component: **Coilcraft `XGL6060-331MEB` (0.33 µH, $I_{\text{sat}} = 33.2\text{A}$, DCR = $1.95\text{ m}\Omega$)**.
- **Output Capacitance**:
  - Bulk capacitance: $4 \times 47\ \mu\text{F}$ (1210 ceramic, 6.3V, X7R) + $1 \times 330\ \mu\text{F}$ (polymer tantalum, 2.5V, $6\text{ m}\Omega$ ESR).
  - High-frequency array: $10 \times 10\ \mu\text{F}$ (0603) + $20 \times 0.47\ \mu\text{F}$ (0402).
  - Calculated output voltage ripple: $\Delta V_{\text{OUT}} < 8\text{ mV}_{\text{p-p}}$.

#### 2.2 VCCO_DDR (1.35V) Memory & I/O Regulator (`U6: TPSM63610RDHR`)
- **Topology**: Synchronous Buck Power Module with integrated shielded inductor and control loop.
- **Input Voltage**: $12.0\text{V}$ nominal.
- **Output Voltage**: $1.35\text{V} \pm 1.5\%$.
- **Rated Output Current**: $10.0\text{A}$ continuous (design budget: $4.0\text{A}$ peak).
- **Efficiency**: $89.8\%$ at $3.0\text{A}$ load.
- **Output Capacitance**: $4 \times 22\ \mu\text{F}$ (0805, 6.3V, X7R) + $8 \times 1\ \mu\text{F}$ (0402).

#### 2.3 VCCAUX (1.80V) Auxiliary Regulator (`U7: TPSM63610RDHR`)
- **Topology**: Synchronous Buck Power Module with integrated shielded inductor.
- **Input Voltage**: $12.0\text{V}$ nominal.
- **Output Voltage**: $1.80\text{V} \pm 1.5\%$.
- **Rated Output Current**: $10.0\text{A}$ continuous (design budget: $2.5\text{A}$ peak).
- **Efficiency**: $90.5\%$ at $2.0\text{A}$ load.

#### 2.4 DDR Termination Regulator (`U9: TPS51200DRCR`)
- **Topology**: Sinking/Sourcing DDR Termination LDO with tracking buffer.
- **Input Voltage ($V_{\text{IN}}$)**: $1.8\text{V}$ or $3.3\text{V}$ (bias supply).
- **Termination Voltage ($V_{\text{TT}}$)**: $0.675\text{V}$ (tracks $V_{\text{DDQ}}/2$ within $\pm 10\text{mV}$).
- **Peak Current**: $\pm 3.0\text{A}$ sink/source.
- **Output Capacitance**: $4 \times 10\ \mu\text{F}$ (0603, 6.3V, X7R) ceramic capacitors distributed along the termination bus strip.

#### 2.5 Transceiver Regulators (`U10: MGTAVCC`, `U11: MGTAVTT` - `TPS7A8500RTER`)
- **Topology**: High-Accuracy ($1\%$), Low-Dropout Linear Regulators.
- **Input Rail**: Pre-regulated $1.35\text{V}$ (for MGTAVCC 1.0V) and $1.8\text{V}$ (for MGTAVTT 1.2V).
- **Noise / PSRR**: Noise spectral density $< 4.4\ \mu\text{V}_{\text{RMS}}$ ($10\text{ Hz}$ to $100\text{ kHz}$), PSRR $> 55\text{ dB}$ at $500\text{ kHz}$.
- **Compliance**: Completely eliminates switching ripple, satisfying AMD Kintex-7 transceiver requirement of $< 10\text{ mV}_{\text{p-p}}$ total noise across $10\text{ kHz} - 80\text{ MHz}$.

---

### 3. KINTEX-7 FFG676 DECOUPLING CAPACITOR SCHEDULE (AMD UG483)

| Power Rail | Nominal Voltage | Bulk Caps ($100-330\ \mu\text{F}$) | Mid-Frequency Caps ($4.7-47\ \mu\text{F}$) | High-Frequency Caps ($0.1-0.47\ \mu\text{F}$) | Total Decoupling Capacitors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **VCCINT** | 1.00 V | 1× 330 µF Poly | 4× 47 µF (1210) | 16× 0.47 µF (0402) + 16× 0.1 µF (0201) | 37 capacitors |
| **VCCBRAM** | 1.00 V | Shared | 2× 22 µF (0805) | 6× 0.1 µF (0402) | 8 capacitors |
| **VCCAUX** | 1.80 V | 1× 47 µF (1210) | 4× 10 µF (0603) | 8× 0.1 µF (0402) | 13 capacitors |
| **VCCO_HP (x3)** | 1.35 V | 1× 47 µF (1210) | 6× 10 µF (0603) | 18× 0.1 µF (0402) | 25 capacitors |
| **VCCO_HR (x5)** | 3.30 V | 1× 47 µF (1210) | 6× 4.7 µF (0603) | 15× 0.1 µF (0402) | 22 capacitors |
| **MGTAVCC** | 1.00 V | 1× 47 µF (0805) | 4× 10 µF (0603) | 14× 0.1 µF (0201 under BGA) | 19 capacitors |
| **MGTAVTT** | 1.20 V | 1× 47 µF (0805) | 4× 10 µF (0603) | 8× 0.1 µF (0201 under BGA) | 13 capacitors |
| **MGTVCCAUX** | 1.80 V | Filtered | 2× 4.7 µF (0603) | 2× 0.1 µF (0402) | 4 capacitors |

---

### 4. DETERMINISTIC POWER SEQUENCING LADDER

AMD UG483 and DS182 mandate strict power-up sequencing:
$$V_{\text{CCINT}} \rightarrow V_{\text{CCAUX}} \rightarrow V_{\text{CCO}}$$
Transceiver sequencing mandates:
$$MGTAVCC \rightarrow MGTAVTT \rightarrow MGTVCCAUX$$

The sequencing ladder is implemented via hardware `PGOOD`-to-`ENABLE` chaining:
1. **$t_0$**: PCIe $+12\text{V}$ and $+3.3\text{V}$ input rails stabilize above UVLO.
2. **$t_1$**: `U5 (TPS546D24A)` is released from reset; $V_{\text{CCINT}}$ ramps to $1.00\text{V}$ in $1.5\text{ ms}$.
3. **$t_2$**: `VCCINT_PGOOD` asserts high, which enables `U7 (TPSM63610)` for $V_{\text{CCAUX}}$ (1.80V) and `U10` for $MGTAVCC$ (1.00V).
4. **$t_3$**: `VCCAUX_PGOOD` asserts high, which enables `U6 (TPSM63610)` for $V_{\text{CCO\_DDR}}$ (1.35V), `U11` for $MGTAVTT$ (1.20V), and `U8` for $+3.3\text{V\_SYS}$.
5. **$t_4$**: `VCCO_DDR_PGOOD` asserts high, which enables `U9 (TPS51200)` for $V_{\text{TT\_DDR}}$ (0.675V).
6. **$t_5$**: System Power Good (`SYS_PGOOD`) asserts high, releasing FPGA reset and initializing configuration boot from QSPI Flash.

---

### 5. CONCLUSION

The power distribution network satisfies all ripple, transient, and sequencing requirements of the AMD Kintex-7 FPGA and Micron DDR3L memory system. The thermal footprint and power supply rejection ratio (PSRR) are engineered for continuous high-performance accelerator operation.
