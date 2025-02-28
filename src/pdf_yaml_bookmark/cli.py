import argparse
import os
import re
import sys

import pdf_yaml_bookmark.common
import pdf_yaml_bookmark.bkm_to_gs
import pdf_yaml_bookmark.run_gs

def main():
    parser = argparse.ArgumentParser(
        prog="pdfoutline.py",
        description='Adds table of contents to a PDF document.',
        epilog="Example toc file at https://github.com/yutayamamoto/pdfoutline")
    parser.add_argument('in_pdf', metavar = 'pdf_in', help = 'Input pdf file')
    parser.add_argument('in_toc', metavar = 'toc_in', help = 'Table of contents file in the specified format')
    parser.add_argument('-o', '--output', required = True, metavar = 'pdf_out', help = 'Output pdf file')
    parser.add_argument('-g', '--gs-path', type=str, help = "Path to ghostscript executable", default='gs')
    parser.add_argument('-s', '--show-progress', action = 'store_true', help = "Show progress bar")
    args = parser.parse_args()

    if args.in_pdf == args.output:
        common.eprint('Error: specify different names for input and output files.')
        sys.exit(-1)

    gs_script = bkm_to_gs.bkm_to_gs(args.in_toc)
    run_gs.run_gs(args.in_pdf, gs_script, args.output, gs_path=args.gs_path, show_progress=args.show_progress)

if __name__ == '__main__':
    main()
