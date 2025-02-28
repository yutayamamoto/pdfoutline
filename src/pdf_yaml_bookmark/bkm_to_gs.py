import re
import sys

import common

def bkm_to_gs(bkm_filename):
    if not common.check_readability(bkm_filename):
        sys.exit(-1)

    with open(bkm_filename) as f:
        toc = f.read()
        gs_script = elist_to_gs(toc_to_elist(toc, bkm_filename))
    return gs_script

class Entry():
    def __init__(self, name, page, children):
        self.name = name
        self.page = page
        self.children = children # Entry list

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

def toc_to_elist(toc, filename):
    tab = "" # indentation character(s) evaluated and assigned to this later
    lines = toc.split('\n')
    lineno = 0 # incremented at the very beginning of the loop
    cur_entry = [[]] # current entries by depth
    offset = 0

    for line in lines:
        lineno += 1

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
            (name, page) = re.findall(r'(.*)\s+(\d+)$', line)[0]
            name = name.strip()
            page = int(page) + offset
            cur_entry = cur_entry[:depth+1] + [[]]
            cur_entry[depth].append(Entry(name, page, cur_entry[depth+1]))

        except IndexError:
            common.eprint('{}: line {}: syntax error: {}'.format(filename, lineno, line))
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

