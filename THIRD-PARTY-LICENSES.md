# Third-Party Licenses

Lacerta is licensed under the [Apache License 2.0](LICENSE). This file lists the third-party components that the
repository includes or depends on, with their licenses. The attributions that some of those licenses ask to be
preserved are in [NOTICE](NOTICE). Licenses are those published by each project; check the version you use.

## Included in this repository

| Component | Where | License |
|---|---|---|
| Caravel User Project template (Efabless) | `verilog/dv`, `verilog/includes`, Caravel-derived files in `verilog/rtl`, `Makefile`, `dv_setup`, `openlane` | Apache-2.0 |
| `openlane/Makefile` (adapted from the Caravel User Project by UmbraLogic Technologies LLC) | `openlane/` | Apache-2.0 |
| PicoRV32 | `verilog/rtl_old3/debug/soc/picorv32/picorv32.v` | ISC |
| SkyWater SKY130 standard cells | Generated `gds`, `def`, `lef`, `lib`, `spef`, `mag`, `verilog/gl`, `signoff` | Apache-2.0 |
| KiCad standard footprints | `PCB/Lacerta_v2_1.kicad_pcb` | CC-BY-SA-4.0 with the KiCad library exception |
| Quartus project files | `Interface_Design_Software/development_files/fpga/` | Intel license notice in the file headers |
| Mifral documentation theme (CSS, templates, icons) | `documentation/sphinx/` | Apache-2.0 (Mifral Tech S.A. de C.V.) |

## Interface Design Software

| Component | License |
|---|---|
| PySide6 (Qt for Python) and Qt | LGPL-3.0 |
| Pillow | MIT-CMU (HPND) |
| NumPy | BSD-3-Clause |
| pyserial | BSD-3-Clause |
| Python | PSF-2.0 |
| xPack GNU RISC-V Embedded GCC (external toolchain, not stored in the repository) | GPL-3.0-or-later with the GCC Runtime Library Exception |

## Design flow tools (not distributed)

| Tool | License |
|---|---|
| Caravel | Apache-2.0 |
| Caravel management SoC (`mgmt_core_wrapper`) | Apache-2.0 |
| SkyWater SKY130 PDK | Apache-2.0 |
| OpenLane / LibreLane | Apache-2.0 |
| ChipFoundry CLI (`chipfoundry-cli`) | Apache-2.0 |
| Yosys | ISC |
| OpenROAD | BSD-3-Clause |
| Magic | Permissive (custom text) |
| Netgen | Permissive (custom text) |
| KLayout | GPL-3.0 |
| Icarus Verilog | GPL-2.0 |
| Verilator | LGPL-3.0 or Artistic-2.0 |
| cocotb | BSD-3-Clause |
| Docker Engine | Apache-2.0 |

## Documentation site

| Component | License |
|---|---|
| Sphinx | BSD-2-Clause |
| myst-parser | MIT |
| pydata-sphinx-theme | BSD-3-Clause |
| sphinx-autobuild | MIT |
| docutils | Public domain / BSD-2-Clause |
| Bootstrap (bundled in the theme) | MIT |
| Font Awesome Free (bundled in the theme) | Icons CC-BY-4.0, fonts SIL OFL-1.1, code MIT |
| Pygments (code highlighting styles) | BSD-2-Clause |

## Trademarks

"Mifral", "Lacerta" and the Mifral "M" icon are not licensed for reuse by the Apache License (section 6 excludes trademarks).
Caravel, ChipFoundry, Efabless, SkyWater, Infineon, FTDI, Intel, KiCad and Qt belong to their owners and are mentioned only to
identify compatible parts, tools and services.
