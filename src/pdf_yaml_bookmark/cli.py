import argparse
import os
import re
import sys

import pdf_yaml_bookmark.common as common
import pdf_yaml_bookmark.run_gs as run_gs
import pdf_yaml_bookmark.bkm_to_yaml as bkm_to_yaml
import pdf_yaml_bookmark.yaml_to_gs as yaml_to_gs

def main():
    parser = argparse.ArgumentParser(
        prog="pdfoutline.py",
        description='Adds bookmark (table of contents) to a PDF document.',
        epilog="Example bookmark file at https://github.com/yutayamamoto/pdfoutline")
    parser.add_argument('in_pdf', metavar = 'pdf_in', help = 'Input pdf file')
    parser.add_argument('in_bkm', metavar = 'bkm_in', help = 'Table of contents file in the specified format')
    parser.add_argument('-o', '--output', required = True, metavar = 'pdf_out', help = 'Output pdf file')
    parser.add_argument('-g', '--gs-path', type=str, help = "Path to ghostscript executable", default='gs')
    parser.add_argument('-f', '--format', type=str, help = 'A format of bookmark file ["bkm","yaml"]')
    parser.add_argument('-e', '--export-yaml', type=str, help = "Path to export bookmark file in YAML format")
    parser.add_argument('-s', '--show-progress', action = 'store_true', help = "Show progress bar")
    args = parser.parse_args()

    if args.in_pdf == args.output:
        common.eprint('Error: specify different names for input and output files.')
        sys.exit(-1)

    bkm_filename = args.in_bkm
    if not common.check_readability(bkm_filename):
        sys.exit(-1)

    # Read bookmark in YAML format
    if args.format == "yaml":
        with open(bkm_filename) as f:
            yaml = f.read()
    else:
        with open(bkm_filename) as f:
            bkm = f.read()
            yaml = bkm_to_yaml.bkm_to_yaml(bkm)

    # Create GS script
    gs = yaml_to_gs.yaml_to_gs(yaml)

    # Run GS
    run_gs.run_gs(args.in_pdf, gs, args.output, gs_path=args.gs_path, show_progress=args.show_progress)

if __name__ == '__main__':
    main()
