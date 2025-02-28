import os
import re
import shutil
import subprocess
import sys
import tempfile

import pdf_yaml_bookmark.common as common

def run_gs(inpdf, gs_script, outpdf, gs_path='gs', show_progress=False):
    if not common.check_readability(inpdf):
        sys.exit(-1)

    if not shutil.which(gs_path):
        common.eprint('Ghostscript executable "{}" not found'.format(gs_path))
        sys.exit(-1)

    tmp = tempfile.NamedTemporaryFile(mode = 'w', delete=False)
    tmp.write(gs_script)
    tmp.close()

    process = subprocess.Popen(\
        [gs_path, '-o', outpdf, '-sDEVICE=pdfwrite', tmp.name, '-f', inpdf],\
        stdout=subprocess.PIPE)

    # show progress bar
    totalPage = 0
    for line in process.stdout:
        tot = re.findall(r'Processing pages 1 through (\d+)', line.decode('ascii'))
        if tot:
            totalPage = int(tot[0])
            if show_progress:
                printProgressBar(0, totalPage)
            break

    for line in process.stdout:
        currentPage = re.findall(r'Page (\d+)', line.decode('ascii').strip())
        if currentPage and show_progress:
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
    print("\r{} |{}| {}/{} {}".format(prefix, bar, iteration, total, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
