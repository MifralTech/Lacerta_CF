# Proposed Solution

Lacerta proposes an open hardware platform designed to simplify the creation of graphical interfaces for embedded systems by moving the interface generation process from software to dedicated hardware. The platform introduces a configurable interface rendering engine implemented as a custom ASIC integrated within the Caravel SoC user project area.

Instead of requiring developers to manually program complex graphical interfaces in firmware, Lacerta allows the interface to be **visually designed using a graphical configuration tool**. This tool enables users to place graphical elements such as buttons, bars, numeric indicators, and status displays within a virtual layout that represents the final interface.

Once the interface is designed, the configuration is exported as a description file. This configuration is then transmitted to the Lacerta hardware engine via the **UART interface**, allowing the ASIC to be easily configured and updated from any compatible host system. The ASIC interprets this configuration and generates the graphical output in real time.

## Hardware-Based Interface Rendering

The Lacerta ASIC includes a hardware rendering engine capable of generating graphical interface components directly in hardware. This approach significantly reduces the computational burden typically placed on embedded processors.

By implementing the interface generation logic in dedicated hardware, Lacerta provides several advantages:

- deterministic graphical rendering  
- reduced firmware complexity  
- lower processor utilization  
- improved system responsiveness  
- simplified integration with UART-based embedded systems

The generated interface is transmitted to a display through an **SPI TFT/OLED output**, enabling the system to drive compact embedded screens commonly used in modern devices, without requiring external graphics processors.

## Integration with Embedded Systems

Lacerta is designed to receive data through a **UART interface**, allowing real-world system information to be visualized through the graphical interface.

In its current architecture, Lacerta does not directly acquire analog or heterogeneous digital signals. Instead, the required data must be formatted as UART messages by an external microcontroller, preprocessing stage, or interface circuit before being sent to the ASIC.

Once received through UART, the data is interpreted by the Lacerta interface engine and mapped to graphical elements such as bars or numeric indicators, enabling real-time visualization of system parameters.

:::{figure} ../assets/img/flow_inputs.png
:alt: Example of system data being adapted into UART messages before reaching the Lacerta platform
:align: center

**Figure 3.** Example of system data being adapted into UART messages before reaching the Lacerta platform, where the interface engine updates graphical elements in real time.
:::

## Interface Design Workflow

The Lacerta platform introduces a streamlined workflow for creating embedded graphical interfaces:

1. **Interface Design**  
   A graphical design tool allows users to create a custom interface layout using predefined visual components.

2. **Configuration Generation**  
   The tool exports a configuration file describing the interface structure and graphical element parameters.

3. **Hardware Deployment via UART**  
   The configuration is sent to the Lacerta hardware engine through the UART interface, enabling easy and flexible configuration of the ASIC.

4. **Runtime Visualization**  
   Incoming UART data dynamically updates the graphical elements rendered by the hardware. If the original source is not UART, external circuitry or firmware must convert it beforehand.

This workflow allows developers to design complex interfaces without writing extensive display control firmware.

:::{figure} ../assets/img/Flow_interfacev2.png
:alt: Lacerta interface creation workflow
:align: center

**Figure 4.** Lacerta interface creation workflow. A graphical editor is used to design custom interface layouts, which are translated into configuration data and transmitted via UART to the Lacerta hardware engine to generate the graphical display.
:::


## Open and Reproducible Architecture

Lacerta is designed as a **fully open-source reference architecture**. The project includes all required design artifacts to reproduce the system, including:

- Documentation (Current file)
- [RTL source code for the ASIC implementation](https://github.com/MifralTech/Lacerta_CF/tree/main/verilog/rtl)
- [Librelane physical design flow integration](https://github.com/MifralTech/Lacerta_CF/tree/main/openlane)  
<!--- [Verification testbenches]()  -->
- [PCB design files](https://github.com/MifralTech/Lacerta_CF/tree/main/PCB)
- [Firmware examples](https://github.com/chipfoundry/caravel_board)  
- [Interface design tools](https://github.com/MifralTech/Lacerta_CF/tree/main/Interface_Design_Software)

By providing an open and reproducible platform, Lacerta enables developers, researchers, and educators to build customizable embedded human–machine interfaces for industrial, commercial, and edge-IoT applications.
