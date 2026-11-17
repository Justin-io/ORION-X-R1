# SYSTEM SIGNAL FLOW & BUS ARCHITECTURE
## Project: ORION-X R1.0
## Classification: High-Density FPGA Computing & PCIe Accelerator PCB
## Document ID: ARCH-SIG-001

---

### 1. HIGH-SPEED COMPUTING PIPELINE DATAFLOW

```mermaid
sequenceDiagram
    autonumber
    participant Host as Host PC (CPU / Root Complex)
    participant Edge as PCIe x4 Connector (J1)
    participant GTX as Kintex-7 GTX Quad 115 (PCIE_X0Y0)
    participant Core as Accelerator Engine (FPGA Logic)
    participant MIG as 7-Series MIG Memory Controller
    participant DRAM as DDR3L Memory (U2 + U3, 32-bit)

    Host->>Edge: PCIe Gen2 TLP Request (5.0 GT/s, Memory Write / DMA)
    Edge->>GTX: Differential CML Data via AC Coupling Caps
    GTX->>Core: AXI4-Stream / AXI4 Memory-Mapped Master Transactions
    Core->>Core: High-Throughput Compute Acceleration Pipeline (DSP48E1 / Logic)
    Core->>MIG: Native AXI4 Read/Write Commands (512-bit / 256-bit wide)
    MIG->>DRAM: 32-bit DDR3L Transactions (DQ[31:0], DQS, Fly-by Addr/Ctrl @ 800MHz)
    DRAM-->>MIG: Low-Latency Read Data Burst
    MIG-->>Core: Processed Vector / Matrix Acceleration Operands
    Core->>GTX: Result TLPs via PCIe Hard IP DMA Engine
    GTX->>Edge: High-Speed Differential Serial Return
    Edge->>Host: PCIe Host Interrupt / Completion TLP Received
```

---

### 2. CONFIGURATION & BOOT SIGNAL FLOW

1. **Power Stabilization**: All power rails ramp via the hardware PGOOD ladder.
2. **Reset Release**: Once `+3.3V_SYS` stabilizes, `PROGRAM_B_0` is pulled high by a $4.7\text{ k}\Omega$ resistor.
3. **Mode Sampling**: Mode pins `M[2:0]` are sampled by Bank 0 logic. Configured to `001` (Master SPI x4 mode).
4. **Flash Initialization**: The FPGA internal configuration master drives `CCLK` (initially at ~3 MHz) and asserts `FCS_B` low to `U4 (Macronix MX25L25645G)`.
5. **Bitstream Ingestion**: Fast Read Quad Output opcode (`0x6B` or `0xEB`) is issued, streaming bitstream data across `D[3:0]` into FPGA Bank 14 at up to 66 MHz.
6. **Done Transition**: Once bitstream CRC is validated, FPGA releases `DONE_0` (open-drain, pulled high to 3.3V via $330\ \Omega$ + Green LED).
7. **PCIe Link Training**: Integrated PCIe block enters LTSSM Detect state, detects host receiver termination, and transitions through Polling to L0 state at Gen1 (2.5 GT/s), auto-negotiating to Gen2 (5.0 GT/s).
8. **MIG Calibration**: DDR3 controller performs write leveling, read DQS centering, and multi-rank calibration against DRAM devices `U2` and `U3`. `CALIB_DONE` LED illuminates green. Accelerator card is fully online.

