import argparse
import os
from pathlib import Path
import re
import sys

import typer

import pdf_yaml_bookmark.common as common
import pdf_yaml_bookmark.run_gs as run_gs
import pdf_yaml_bookmark.bkm_to_yaml as bkm_to_yaml
import pdf_yaml_bookmark.yaml_to_gs as yaml_to_gs

app = typer.Typer()

@app.command()
def cli(
    input_pdf: Path = typer.Argument(..., help="Input PDF file"),
    bookmark_file: Path = typer.Option(..., "-b", "--bookmark", help="Bookmark file (.bkm or .yaml/.yml)"),
    output_pdf: Path = typer.Option(..., "-o", "--output", help="Output PDF file"),
    export_yaml: Path = typer.Option(None, "--export-yaml", help="Export intermediate YAML"),
    show_progress: bool = typer.Option(False, "--show-progress", help="Show progress bar"),
    gs_path: Path = typer.Option("gs", "--gs-path", help="A path to ghostscript executable")
):
    if input_pdf == output_pdf:
        common.eprint('Error: specify different names for input and output files.')
        sys.exit(-1)

    if not common.check_readability(bookmark_file):
        sys.exit(-1)

    # Identify the format of the bookmark file
    if bookmark_file.suffix in [".yaml", ".yml"]:
        with open(bookmark_file) as f:
            yaml = f.read()
    else:
        with open(bookmark_file) as f:
            bkm = f.read()
            yaml = bkm_to_yaml.bkm_to_yaml(bkm)
        if export_yaml:
            with open(export_yaml, "w") as f:
                f.write(yaml)

    # Create GS script
    gs = yaml_to_gs.yaml_to_gs(yaml)

    # Run GS
    run_gs.run_gs(input_pdf, gs, output_pdf, gs_path=gs_path, show_progress=show_progress)

if __name__ == "__main__":
    app()
