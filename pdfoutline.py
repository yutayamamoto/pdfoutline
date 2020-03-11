#!/usr/bin/python3

# https://www.planetpdf.com/planetpdf/pdfs/primer.pdf
# https://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/pdfmarkreference.pdf
# in toc file, you must close the parenthesis()!! otherwise, gs fails.


import sys
import re
import subprocess


class Entry():

    def __init__(self, name, page, children):
        self.name = name
        self.page = page
        self.children = children # Entry list

    def pritty_print(self, depth):
        print(depth * '  ' + self.name + ':' + str(self.page))
        for c in self.children:
            c.pritty_print(depth+1)


def toc_to_elist(toc, TAB = '    '):

    lines = list(filter(bool, toc.split('\n'))) # filter empty string
    cur_entry = [[]] # current entries by depth
    offset = 0

    for line in lines:

        depth = line.count(TAB)
        line = line.split('#')[0].strip() # strip comments and white spaces

        if not line:
            continue

        if line[0] in '+-':
            offset += int(line[1:])
            continue

        try:
            (name, page) = re.findall(r'(.*) (\d+)$', line)[0]
            page = int(page) + offset
            cur_entry = cur_entry[:depth+1] + [[]]
            cur_entry[depth].append(Entry(name, page, cur_entry[depth+1]))

        except:
            print('syntax error in toc-file. line:\n' + line)
            exit(1)

    return cur_entry[0]


def elist_to_gs(elist):

    def rec_elist_to_gslist(elist):
        gs_list = []
        for entry in elist:
            gs_list.append("[/Page %d /View [/XYZ null null null] /Title (%s) /Count %d /OUT pdfmark" \
                    % (entry.page, entry.name, len(entry.children)))
            gs_list += rec_elist_to_gslist(entry.children)
        return gs_list

    return '\n'.join(rec_elist_to_gslist(elist))


def pdfoutline(inpdf, tocfilename, outpdf):

    with open(tocfilename) as f:
        toc = f.read()
        gs_command = elist_to_gs(toc_to_elist(toc))

    with open('/tmp/tmp.gs', 'w') as out:
        out.write(gs_command)

    process = subprocess.Popen(\
        ['gs', '-o', outpdf, '-sDEVICE=pdfwrite', '/tmp/tmp.gs' , '-f', inpdf],\
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

    if len(sys.argv) == 4:
        if sys.argv[1] == sys.argv[3]:
            print('Specify different names for input and output files.')
        else:
            pdfoutline(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('usage: pdfoutline in.pdf in.toc out.pdf')
