# Third-Party Licenses

Lacerta is licensed under the [Apache License 2.0](LICENSE). This file lists the third-party
components the repository includes, links to, or needs in order to be built, together with
their licenses. The attributions that those licenses ask to be preserved are repeated in
[NOTICE](NOTICE).

This list was prepared by inspecting the repository. Licenses are those published upstream;
check the exact versions you use. It is not legal advice.

**Summary:** nothing found requires the repository as a whole to change its license. The
points that need attention are marked with ⚠️ and collected in
[Open items](#open-items).

---

## 1. Included in this repository

| Component | Where | License | Notes |
|---|---|---|---|
| Caravel User Project template (Efabless) | `verilog/dv`, `verilog/includes`, Caravel-derived files in `verilog/rtl`, `verilog/rtl_old*`, `Makefile`, `dv_setup`, `openlane` | Apache-2.0 | Same license as this repository. Keep the `SPDX-FileCopyrightText: … Efabless Corporation` headers. |
| `openlane/Makefile` | `openlane/` | Apache-2.0 | Adapted from the Caravel User Project by UmbraLogic Technologies LLC (2025). |
| PicoRV32 | `verilog/rtl_old3/debug/soc/picorv32/picorv32.v` | ISC | Historical code, not part of the current design. Keep the ISC notice in the file. |
| SkyWater SKY130 standard cells | Generated `gds/`, `def/`, `lef/`, `lib/`, `spef/`, `mag/`, `verilog/gl/`, `signoff/` | Apache-2.0 | Embedded by the OpenLane flow in the generated layout and netlist views. |
| `CY7C1049GN.v` (SRAM model) and `uart_bfm.v` (UART bus functional model) | `verilog/dv/lacerta/` | Generated with ChatGPT | ⚠️ Testbench code, not vendor code and not part of the fabricated design. See [Open items](#open-items). |
| KiCad standard footprints | `PCB/Lacerta_v2_1.kicad_pcb` | CC-BY-SA-4.0 with the KiCad library exception | The exception allows the resulting design to use any license. |
| `Caravel_Board` footprints | `PCB/Lacerta_v2_1.kicad_pcb` | Apache-2.0 | From the Efabless/ChipFoundry caravel_board project. |
| `strive_foot_prints` footprints | `PCB/Lacerta_v2_1.kicad_pcb` | ⚠️ Unknown | Origin not documented. See [Open items](#open-items). |
| Quartus project files | `Interface_Design_Software/development_files/fpga/lacerta.qpf`, `lacerta.qsf` | Intel notice | ⚠️ Generated files that carry Intel's license notice; not covered by Apache-2.0. |
| Mifral documentation theme (CSS, templates, design tokens, icons) | `documentation/sphinx/` | Apache-2.0 (Mifral Tech S.A. de C.V.) | Copied from Mifral's own Orbit documentation portal. The logos are trademarks; see below. |

---

## 2. Interface Design Software (GUI)

The GUI is written in Python and uses these runtime libraries:

| Package | License | Notes |
|---|---|---|
| PySide6 (Qt for Python) and Qt | LGPL-3.0 (also offered under GPL and a commercial license) | ⚠️ Permitted with Apache-2.0 if the LGPL conditions are met when distributing the Windows package: keep the Qt/PySide6 license text and let users replace the libraries. Do **not** switch to PyQt5/PyQt6, which are GPL or commercial. |
| Pillow | MIT-CMU (HPND) | Permissive. |
| NumPy | BSD-3-Clause | Permissive. |
| pyserial | BSD-3-Clause | Permissive. |
| Python | PSF-2.0 | Permissive. |

The GUI builds firmware for the on-chip RISC-V core with an external toolchain that is declared in
`Interface_Design_Software/development_files/tools/package.json` and **not** stored in the repository:

| Tool | License | Notes |
|---|---|---|
| xPack GNU RISC-V Embedded GCC (`@xpack-dev-tools/riscv-none-elf-gcc`) | GPL-3.0-or-later with the GCC Runtime Library Exception; newlib under permissive licenses | Used as a separate program. The GPL does not extend to the firmware it compiles. If the toolchain is ever bundled with the Windows package, its license texts and source offer must travel with it. |

The prebuilt package `Interface_Design_Software/exe_file_GUI/*.rar` has **not** been audited. See
[Open items](#open-items).

---

## 3. Tools used by the design flow (not distributed)

These are downloaded or run by `cf setup`, `cf harden`, `cf precheck` and the simulation scripts. Their outputs
do not take on their licenses, and none of them is linked into this repository.

| Tool | License |
|---|---|
| Caravel and `mgmt_core_wrapper` | Apache-2.0 |
| SkyWater SKY130 PDK | Apache-2.0 |
| OpenLane / LibreLane | Apache-2.0 |
| Yosys | ISC |
| OpenROAD | BSD-3-Clause |
| Magic | Permissive (BSD-style) |
| Netgen | Permissive |
| KLayout | GPL-3.0-or-later |
| Icarus Verilog | GPL-2.0 |
| Verilator | LGPL-3.0 or Artistic-2.0 |
| cocotb | BSD-3-Clause |
| ChipFoundry CLI (`chipfoundry-cli`) | ⚠️ Not verified |
| Docker Engine | Apache-2.0 |

---

## 4. Documentation site

Build tools, installed from `requirements-docs.txt` and not redistributed in the repository:

| Package | License |
|---|---|
| Sphinx | BSD-2-Clause |
| myst-parser | MIT |
| pydata-sphinx-theme | BSD-3-Clause |
| sphinx-autobuild | MIT |
| docutils | Public domain / BSD-2-Clause |

The generated site does contain files from the theme: Bootstrap (MIT), Font Awesome Free (icons CC-BY-4.0, fonts
SIL OFL-1.1, code MIT) and Pygments styles (BSD-2-Clause). Their license headers are kept in the shipped files.

Videos on the demo page are embedded from YouTube and remain subject to YouTube's terms.

---

## 5. Trademarks and brand assets

"Mifral", "Lacerta" and the Mifral "M" icon are not licensed for reuse by the Apache License; section 6 excludes trademarks.
Caravel, ChipFoundry, Efabless, SkyWater, Infineon, FTDI, Intel, KiCad and Qt belong to their owners and are mentioned only
to identify compatible parts, tools and services.

---

## Compatibility notes

- **Apache-2.0 with permissive code (ISC, BSD, MIT):** compatible; keep the copyright and permission notices.
- **LGPL-3.0 (PySide6/Qt):** compatible when the GUI uses the libraries as separate, replaceable components.
- **GPL tools (KLayout, Icarus, GCC):** run as separate programs; they do not affect the license of the design or its outputs.
- **CC-BY-SA-4.0 footprints:** the KiCad library exception lets the board design be distributed under this repository's license.

---

## Open items

1. ⚠️ **`strive_foot_prints` footprint library.** Its origin is not documented (two footprints, `SOIC127P790X216-8N` and
   `SOT65P210X110-5N`). Footprints from component vendors or download sites often have their own terms. Identify the source
   and record its license here, or redraw the footprints.
2. ⚠️ **Windows package (`exe_file_GUI`).** Confirm what is bundled (Python, Qt/PySide6, the RISC-V toolchain). If it is built as a
   single file, check that the LGPL conditions for Qt/PySide6 can be met, and add the license texts to the package.
3. ⚠️ **Quartus files.** The Intel notice in `lacerta.qpf` and `lacerta.qsf` is kept as is. If only the design description is
   needed, consider removing these generated files from the repository and documenting how to regenerate them.
4. ⚠️ **`CY7C1049GN.v` and `uart_bfm.v`.** Both were produced with a generative AI tool and then edited by the authors.
   Copyright in such output is uncertain, so the authors should review them. They are only used in simulation (the testbench
   `verilog/dv/lacerta/lacerta_tb.v` uses both). If preferred, replace them with a vendor model from Infineon or
   with code written by the authors.
5. **Ownership and holder line.** The copyright holder in [NOTICE](NOTICE) is "The Lacerta Authors". Once the co-authorship
   agreement between the authors and Mifral Tech S.A. de C.V. is signed, update it and add SPDX headers to the repository's own
   RTL files (only 3 of 29 files in `verilog/rtl` carry one today).
6. **Images and logos** in `docs/assets/img` (for example `Lacerta2.png` and `lizard_chip.png`): confirm the authors own them or
   have permission, and note if any was produced with a generative tool.
7. **Tool and library versions.** The GUI's Python packages are not pinned in the repository. Pin them (for example in a
   `requirements.txt`) so this file can state exact versions.
