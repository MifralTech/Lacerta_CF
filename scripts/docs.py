#!/usr/bin/env python3
"""Build, serve, and validate the Lacerta Sphinx documentation.

    python scripts/docs.py build     # build English (site root) and Spanish (es/)
    python scripts/docs.py serve     # live-reload preview, English on :8001, Spanish on :8003
    python scripts/docs.py check     # link/parity check, then a strict build of both languages

Warnings are treated as errors (``-W``), so a broken link, missing image, or page that is
not part of a toctree fails the build.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPHINX_ROOT = ROOT / "documentation" / "sphinx"
BUILD_ROOT = ROOT / "build" / "docs"
SITE_ROOT = BUILD_ROOT / "site"

# language -> (source tree, output directory, live-preview port)
LANGUAGES = {
    "en": (ROOT / "docs" / "en", SITE_ROOT, 8001),
    "es": (ROOT / "docs" / "es", SITE_ROOT / "es", 8003),
}


def run(command: list[str], *, env: dict[str, str] | None = None) -> None:
    subprocess.run(command, cwd=ROOT, env=env, check=True)


def clean(path: Path) -> None:
    resolved = path.resolve()
    if not resolved.is_relative_to(BUILD_ROOT.resolve()):
        raise RuntimeError(f"Refusing to clean output outside {BUILD_ROOT}")
    if resolved.exists():
        shutil.rmtree(resolved)


def sphinx_env(language: str) -> dict[str, str]:
    env = dict(os.environ)
    env["LACERTA_DOCS_LANGUAGE"] = language
    return env


def sphinx_args(language: str) -> list[str]:
    source, output, _ = LANGUAGES[language]
    return [
        "-b",
        "html",
        "-W",
        "--keep-going",
        "-c",
        str(SPHINX_ROOT),
        "-d",
        str(BUILD_ROOT / ".doctrees" / language),
        str(source),
        str(output),
    ]


def build() -> None:
    clean(SITE_ROOT)
    clean(BUILD_ROOT / ".doctrees")
    # English first: the Spanish site is written inside it, under es/.
    for language in ("en", "es"):
        run([sys.executable, "-m", "sphinx", *sphinx_args(language)], env=sphinx_env(language))
    # GitHub Pages runs Jekyll unless told otherwise, which would drop _static and _images.
    (SITE_ROOT / ".nojekyll").touch()


def serve() -> int:
    build()
    processes: list[subprocess.Popen[bytes]] = []
    try:
        for language, (_, _, port) in LANGUAGES.items():
            command = [
                sys.executable,
                "-m",
                "sphinx_autobuild",
                *sphinx_args(language),
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
                "--watch",
                str(SPHINX_ROOT),
                "--watch",
                str(ROOT / "docs" / "assets"),
                "--ignore",
                "*/__pycache__/*",
                "--ignore",
                "*.pyc",
            ]
            processes.append(subprocess.Popen(command, cwd=ROOT, env=sphinx_env(language)))
        return processes[0].wait()
    finally:
        for process in processes:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


def check() -> None:
    run([sys.executable, "scripts/check_doc_links.py"])
    build()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("build", "serve", "check"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "build":
        build()
    elif args.command == "serve":
        return serve()
    else:
        check()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130) from None
