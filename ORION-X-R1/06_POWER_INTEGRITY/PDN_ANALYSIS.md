# ORION-X R1 — POWER DISTRIBUTION NETWORK (PDN) ANALYSIS

## 1. Executive Summary & Design Scope
The ORION-X R1 computing accelerator platform incorporates high-performance AMD Kintex-7 FPGA logic (`XC7K160T-2FFG676C`), dual x16 DDR3L SDRAM memory running at 800 MHz (1600 MT/s), and PCIe Gen2 x4 multi-gigabit transceivers. 

To maintain signal integrity and prevent supply-induced jitter or logic errors, the Power Distribution Network (PDN) is engineered with targeted target-impedance constraints ($Z_{target}$) across the frequency domain from DC up to 200 MHz.

---

## 2. Power Rail Budget & Target Impedance Calculations

Target impedance is defined as:
$$Z_{target} = \frac{V_{rail} \times \Delta V_{ripple, max}}{I_{transient, max}}$$

Where:
- $V_{rail}$: Nominal operating voltage
- $\Delta V_{ripple, max}$: Allowable ripple percentage (typically $\pm 3\%$ for Core/Transceivers, $\pm 5\%$ for I/O)
- $I_{transient, max}$: Estimated peak transient step current (assumed 50% of maximum rail current)

| Rail Identifier | Nominal Voltage | $I_{max}$ (A) | $\Delta I_{transient}$ (A) | Allowable Ripple ($\pm\%$) | Max Ripple ($\text{mV}$) | $Z_{target}\ (\text{m}\Omega)$ | Primary Regulator |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **VCCINT** | 1.00 V | 30.0 A | 15.0 A | $\pm 3\%$ | 30 mV | **2.0 m$\Omega$** | TPS546D24ARVFR (40A PMBus Buck) |
| **VCCO_DDR** | 1.35 V | 6.0 A | 3.0 A | $\pm 4\%$ | 54 mV | **18.0 m$\Omega$** | TPSM63610RDHR (10A Module) |
| **VCCAUX** | 1.80 V | 4.0 A | 2.0 A | $\pm 3\%$ | 54 mV | **27.0 m$\Omega$** | TPSM63610RDHR (10A Module) |
| **+3.3V_SYS** | 3.30 V | 5.0 A | 2.5 A | $\pm 5\%$ | 165 mV | **66.0 m$\Omega$** | TPSM63610RDHR (10A Module) |
| **MGTAVCC** | 1.00 V | 1.8 A | 0.6 A | $\pm 2.5\%$ | 25 mV | **41.7 m$\Omega$** | TPS7A8500RTER (Ultra-Low-Noise LDO) |
| **MGTAVTT** | 1.20 V | 1.5 A | 0.5 A | $\pm 2.5\%$ | 30 mV | **60.0 m$\Omega$** | TPS7A8500RTER (Ultra-Low-Noise LDO) |
| **VTT_DDR** | 0.675 V | 2.5 A | 1.5 A | $\pm 5\%$ | 33.7 mV | **22.5 m$\Omega$** | TPS51200DRCR (Sink/Source LDO) |

---

## 3. Plane Cavity Resonance & Layer Assignment Strategy

### 3.1 Stackup Cavity Analysis
ORION-X employs a 12-layer balanced symmetric stackup:
- **Layer 4**: GND Reference Plane ($35\,\mu\text{m}$)
- **Layer 5**: VCCINT Plane ($35\,\mu\text{m}$)
- **Layer 6**: GND Reference Plane ($35\,\mu\text{m}$)
- **Dielectric Thickness**: $100\,\mu\text{m}$ Panasonic Megtron 6 ($D_k = 3.65, D_f = 0.002$)

The ultra-thin $100\,\mu\text{m}$ dielectric core creates high distributed inter-plane capacitance:
$$C_{plane} = \epsilon_0 \epsilon_r \frac{A}{d} = (8.854 \times 10^{-12}) \times 3.65 \times \frac{0.016\text{ m}^2}{0.0001\text{ m}} \approx 5.17\text{ nF}$$

This dual-GND sandwiched power plane provides:
1. Extremely low plane spreading inductance ($L_{spread} < 15\text{ pH}$).
2. Suppression of parallel-plate standing wave resonances up to 1.2 GHz.
3. Perfect symmetric image charge absorption during nanosecond FPGA logic transitions.

### 3.2 High-Current VCCINT Plane Escape
The 40A TPS546D24ARVFR regulator features a dedicated 12-via thermal and electrical transition matrix connected directly to the Layer 5 VCCINT polygon. With each via featuring a $0.30\text{ mm}$ drill and $25\,\mu\text{m}$ barrel plating, the total DC resistance from regulator output inductor L1 to the FPGA core BGA ball cluster is $< 0.4\text{ m}\Omega$, ensuring $< 12\text{ mV}$ DC IR drop at full 30A load.

---

## 4. Multi-Stage Decoupling Methodology

The decoupling network spans 4 decades of frequency response:
1. **Bulk Stage ($1\text{ kHz} - 100\text{ kHz}$)**:
   - High-capacitance, low-ESR polymer and 1210 ceramic capacitors ($100\,\mu\text{F}, 47\,\mu\text{F}$) located at regulator output stages to absorb load steps and maintain voltage control-loop stability.
2. **Mid-Frequency Stage ($100\text{ kHz} - 10\text{ MHz}$)**:
   - $10\,\mu\text{F}$ and $4.7\,\mu\text{F}$ 0805/0603 X7R MLCCs distributed around the BGA perimeter to sustain charge during burst transactions.
3. **High-Frequency Stage ($10\text{ MHz} - 100\text{ MHz}$)**:
   - $1.0\,\mu\text{F}$ and $0.1\,\mu\text{F}$ 0402 ceramic capacitors placed on the bottom surface (Layer 12) directly underneath the FPGA BGA array, connected to BGA power/ground balls with minimal loop inductance ($L_{loop} < 0.6\text{ nH}$).
4. **Ultra-High Frequency Stage ($> 100\text{ MHz}$)**:
   - Planar inter-dielectric capacitance between Layer 4/5/6 and on-die Kintex-7 trench capacitors.

---

## 5. Verification & Compliance
- **DC IR Drop**: $< 1.2\%$ across all internal power nets.
- **AC Target Impedance**: Satisfied across all rails up to $f_{knee} \approx 200\text{ MHz}$.
- **Transceiver Isolation**: MGTAVCC and MGTAVTT isolated via LDO active ripple rejection ($> 55\text{ dB}$ PSRR at $100\text{ kHz}$) and ferrite beads.

