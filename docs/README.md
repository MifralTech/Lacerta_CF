# Lacerta documentation

The documentation is a single [Sphinx](https://www.sphinx-doc.org/) site in two languages, written in
Markdown ([MyST](https://myst-parser.readthedocs.io/)). English is the site root and Spanish is served
under `/es/`. It is published to GitHub Pages at <https://mifraltech.github.io/Lacerta_CF/>.

```text
docs/
  en/                 English pages (site root)
  es/                 Spanish pages (site /es/) — same file names as en/
  assets/img/         Images shared by both languages
  assets/downloads/   Files linked from the pages (BOM, simulation log, testbench diagram)
documentation/sphinx/ Sphinx configuration, templates and the Mifral theme (CSS, logos)
scripts/docs.py       Build, live preview and checks
requirements-docs.txt Pinned documentation dependencies
```

## Build and preview

```bash
python -m pip install -r requirements-docs.txt
python scripts/docs.py build   # writes build/docs/site (English) and build/docs/site/es (Spanish)
python scripts/docs.py serve   # live preview: English on :8001, Spanish on :8003
python scripts/docs.py check   # link and language-parity check, then a strict build (used by CI)
```

The build treats warnings as errors, so a broken link, a missing image or a page that is not listed in a
`toctree` fails it. Use Python 3.10–3.12.

## Editing rules

- Keep `docs/en` and `docs/es` in step: every page must exist in both languages under the same file name,
  otherwise the language switcher would land on a missing page. `scripts/docs.py check` enforces this.
- Add new pages to the hidden `toctree` in `index.md` and to the navigation in
  `documentation/sphinx/conf.py`.
- Figures use the MyST `figure` directive with paths like `../assets/img/name.png`. Raw `<img>` tags are not
  processed by Sphinx and will not be copied to the site.
- Files in `assets/downloads/` are copied to the site root, so link to them by bare file name with an HTML
  anchor: `<a href="lacerta_bom.csv">lacerta_bom.csv</a>`.
- The authors page (`authors.md`) still has placeholder profile links; replace them with the real profile URLs.
