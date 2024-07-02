#!/usr/bin/python3

# Adobe pdfMark Reference
# https://opensource.adobe.com/dc-acrobat-sdk-docs/acrobatsdk/pdfs/acrobatsdk_pdfmark.pdf

# in toc file, you must close the parenthesis()!! otherwise, gs fails.


import sys
import re
import subprocess
import tempfile, os, sys
import argparse

class Entry():

    def __init__(self, name, page, children):
        self.name = name
        self.page = page
        self.children = children # Entry list

    def pritty_print(self, depth):
        print(depth * '  ' + self.name + ':' + str(self.page))
        for c in self.children:
            c.pritty_print(depth+1)


# Parse the start of the line for whitespace characters and return "tab";
# should only be called once on first occurrence of an indent while tab == ""
def parse_tab(line):
    tab = ""

    # add whitespace characters to tab
    for ch in line:
        if (ch.isspace()):
            tab += ch
        else:
            break

    return tab


def toc_to_elist(toc):

    tab = "" # indentation character(s) evaluated and assigned to this later
    lines = toc.split('\n')
    cur_entry = [[]] # current entries by depth
    offset = 0

    for line in lines:

        # if indentation style hasn't been evaluated yet and the line starts
        # with a whitespace character, assume its an indent and assign all the
        # leading whitespace to tab
        if ((tab == "") and (line != "") and (line[0].isspace())):
            tab = parse_tab(line)

        depth = 0

        # determine depth level of indent
        if (tab != ""):
            # find length of leading whitespace in string
            ws_len = 0
            for ch in line:
                if (ch.isspace()):
                    ws_len += 1
                else:
                    break

            # count indent level up to first non-whitespace character;
            # allows for "indents" to appear inside section titles e.g. if an
            # indent level of a single space was chosen
            depth = line.count(tab, 0, ws_len)

        line = line.split('#')[0].strip() # strip comments and white spaces

        if not line:
            continue

        if line[0] == '+':
            offset += int(line[1:])
            continue

        if line[0] == '-':
            offset -= int(line[1:])
            continue

        try:
            (name, page) = re.findall(r'(.*) (\d+)$', line)[0]
            page = int(page) + offset
            cur_entry = cur_entry[:depth+1] + [[]]
            cur_entry[depth].append(Entry(name, page, cur_entry[depth+1]))

        except:
            # todo display line number
            print('syntax error in toc-file. line:\n' + line)
            exit(1)

    return cur_entry[0]


def elist_to_gs(elist):

    def rec_elist_to_gslist(elist):
        gs_list = []
        for entry in elist:
            gs_list.append("[/Page %d /View [/XYZ null null null] /Title <%s> /Count %d /OUT pdfmark" \
                    % (entry.page, "FEFF" + entry.name.encode("utf-16-be").hex(), len(entry.children)))
            gs_list += rec_elist_to_gslist(entry.children)
        return gs_list

    return '\n'.join(rec_elist_to_gslist(elist))


def pdfoutline(inpdf, tocfilename, outpdf, gs='gs'):

    with open(tocfilename) as f:
        toc = f.read()
        gs_command = elist_to_gs(toc_to_elist(toc))

    tmp = tempfile.NamedTemporaryFile(mode = 'w', delete=False)
    tmp.write(gs_command)
    tmp.close()

    process = subprocess.Popen(\
        [gs, '-o', outpdf, '-sDEVICE=pdfwrite', tmp.name, '-f', inpdf],\
        stdout=subprocess.PIPE)

    # show progress bar
    totalPage = 0
    for line in process.stdout:
        tot = re.findall(r'Processing pages 1 through (\d+)', line.decode('ascii'))
        if tot:
            totalPage = int(tot[0])
            printProgressBar(0, totalPage)
            break

    for line in process.stdout:
        currentPage = re.findall(r'Page (\d+)', line.decode('ascii').strip())
        if currentPage:
            printProgressBar(int(currentPage[0]), totalPage)

    os.unlink(tmp.name)


# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %d/%d %s' % (prefix, bar, iteration, total, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="pdfoutline.py",
        description='Adds table of contents to a PDF document.',
        epilog="Example toc file at https://github.com/yutayamamoto/pdfoutline")

    parser.add_argument('in_pdf', metavar = 'pdf_in', help = 'Input pdf file')
    parser.add_argument('in_toc', metavar = 'toc_in', help = 'Table of contents file in the specified format')
    parser.add_argument('out_pdf', metavar = 'pdf_out', help = 'Output pdf file')
    parser.add_argument('-g', '--gs_path', type=str, help = "Path to ghostscript executable")

    args = parser.parse_args()

    if args.in_pdf == args.out_pdf:
        print('Specify different names for input and output files.')
        sys.exit()
    if args.gs_path :
        pdfoutline(args.in_pdf, args.in_toc, args.out_pdf, args.gs_path)
    else:
        pdfoutline(args.in_pdf, args.in_toc, args.out_pdf)
