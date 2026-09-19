"""Sphinx configuration for the Lacerta documentation site.

One site, two languages. The language is selected with ``LACERTA_DOCS_LANGUAGE``
(``en`` by default, ``es`` for the Spanish tree); ``scripts/docs.py`` builds both and
places the Spanish output under ``es/`` so the language switcher links line up.

The look follows the Mifral documentation portals: ``pydata-sphinx-theme`` with the
Mifral design tokens, a top navigation bar, and a grouped sidebar.
"""

from __future__ import annotations

import os
from pathlib import Path


SPHINX_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SPHINX_ROOT.parents[1]
DOWNLOADS = REPO_ROOT / "docs" / "assets" / "downloads"

LANGUAGE = os.environ.get("LACERTA_DOCS_LANGUAGE", "en")
if LANGUAGE not in {"en", "es"}:
    raise ValueError(f"Unknown documentation language: {LANGUAGE}")

_TEXT = {
    "en": {
        "project": "Lacerta Documentation",
        "sidebar_title": "Contents",
        "language_name": "Español",
        "nav": [
            ("Home", "index"),
            ("Problem", "problem_statement"),
            ("Solution", "proposed_solution"),
            ("Architecture", "system_architecture"),
            ("Development", "system_development"),
            ("GUI and FPGA demo", "lacerta_gui_fpga_demo"),
            ("Appendix", "appendix"),
            ("Authors", "authors"),
        ],
        "groups": [
            (
                "Introduction",
                [
                    ("Overview", "index"),
                    ("Problem statement", "problem_statement"),
                    ("Proposed solution", "proposed_solution"),
                ],
            ),
            (
                "System",
                [
                    ("System architecture", "system_architecture"),
                    ("System development", "system_development"),
                ],
            ),
            (
                "Resources",
                [
                    ("GUI and FPGA demo", "lacerta_gui_fpga_demo"),
                    ("Appendix", "appendix"),
                    ("Authors", "authors"),
                ],
            ),
        ],
    },
    "es": {
        "project": "Documentación de Lacerta",
        "sidebar_title": "Contenido",
        "language_name": "English",
        "nav": [
            ("Inicio", "index"),
            ("Problema", "problem_statement"),
            ("Solución", "proposed_solution"),
            ("Arquitectura", "system_architecture"),
            ("Desarrollo", "system_development"),
            ("GUI y demo en FPGA", "lacerta_gui_fpga_demo"),
            ("Apéndice", "appendix"),
            ("Autores", "authors"),
        ],
        "groups": [
            (
                "Introducción",
                [
                    ("Resumen", "index"),
                    ("Planteamiento del problema", "problem_statement"),
                    ("Solución propuesta", "proposed_solution"),
                ],
            ),
            (
                "Sistema",
                [
                    ("Arquitectura del sistema", "system_architecture"),
                    ("Desarrollo del sistema", "system_development"),
                ],
            ),
            (
                "Recursos",
                [
                    ("GUI y demo en FPGA", "lacerta_gui_fpga_demo"),
                    ("Apéndice", "appendix"),
                    ("Autores", "authors"),
                ],
            ),
        ],
    },
}

_T = _TEXT[LANGUAGE]

project = _T["project"]
# Sphinx appends "documentation" to the project name in <title> unless html_title is set.
html_title = project
author = "Mifral Tech S.A. de C.V."
copyright = "Mifral Tech S.A. de C.V."

extensions = ["myst_parser"]
source_suffix = {".md": "markdown"}
root_doc = "index"
language = LANGUAGE
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

myst_enable_extensions = [
    "attrs_inline",
    "colon_fence",
    "deflist",
    "fieldlist",
    # The pages embed figures as raw <img> tags inside centered <p> blocks.
    # This turns them into Sphinx images so they are found and copied.
    "html_image",
]
myst_heading_anchors = 4
myst_all_links_external = False

templates_path = [str(SPHINX_ROOT / "_templates")]
html_theme = "pydata_sphinx_theme"
html_static_path = [str(SPHINX_ROOT / "_static")]
# Downloadable files (BOM, simulation log, testbench flow diagram) are copied to the
# root of each language build, so pages link to them by bare file name.
html_extra_path = [str(DOWNLOADS)]
html_css_files = [
    "css/mifral-docs-tokens.css",
    "css/lacerta-sphinx.css",
    "css/lacerta-site.css",
]
html_favicon = str(SPHINX_ROOT / "_static/favicon-32.png")
html_sidebars = {"**": ["lacerta-sidebar", "page-toc"]}
html_show_sourcelink = False
html_copy_source = False
html_show_sphinx = True
html_last_updated_fmt = None
pygments_style = "friendly"
pygments_dark_style = "monokai"

html_theme_options = {
    "logo": {
        "text": project,
        "image_light": "mifral-icon-on-light.png",
        "image_dark": "mifral-icon-on-dark.png",
    },
    "navbar_align": "left",
    "navbar_center": ["lacerta-navbar"],
    "navbar_end": ["language-switcher", "theme-switcher"],
    "navbar_persistent": ["search-button-field"],
    "header_links_before_dropdown": 8,
    "primary_sidebar_end": [],
    "secondary_sidebar_items": [],
    "article_header_start": ["breadcrumbs"],
    "article_header_end": [],
    "show_prev_next": True,
    "footer_start": ["mifral-copyright"],
    "footer_center": ["sphinx-version"],
    "footer_end": ["theme-version"],
    "navigation_with_keys": False,
    "show_toc_level": 1,
}

html_context = {
    "lacerta_language": LANGUAGE,
    "lacerta_nav": [
        {"name": name, "doc": doc, "match": doc} for name, doc in _T["nav"]
    ],
    "lacerta_sidebar_groups": [
        {
            "caption": caption,
            "prefixes": [doc for _, doc in items],
            "items": items,
        }
        for caption, items in _T["groups"]
    ],
    "lacerta_language_link": {"name": _T["language_name"]},
    "lacerta_sidebar_title": _T["sidebar_title"],
}
