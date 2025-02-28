import re

def isEmpty(line):
    """
    Returns if a line in the bkm is semantically empty.
    """
    return line.split('#')[0].strip() == ""

def matchOffset(line):
    """
    Returns a match object if it is an "offset directive."
    `.group()` should return a string, expressing an integer, e.g., "+2".
    """
    return re.match(r'^\s*([+-][0-9]*)', line)

def matchSection(line):
    """
    Returns a match object if `line` is writtin in a valid bkm-grammar and
    `None` otherwise.
    The string `line` is expected to have the structure of
    "<indent><heading><spaces><page>". For example, for
    `line = "    A sample title 18"`, `matchSection(line)` should return a
    match object with three groups: "    ", "A sample title", "18".
    """
    return re.match(r'^(\s*)(.*?)\s+([0-9]+)\s*$', line)

def bkm_to_yaml(bkmText):
    bkmText = bkmText.split('\n')
    yamlText = ""
    offset = 0
    linenum = -1
    for line in bkmText:
        linenum += 1

        if isEmpty(line):
            # YAML parser handles empty lines and comments
            yamlText += line + "\n"
            continue

        mo = matchOffset(line)
        if mo:
            offset += int(mo.group())
            continue

        ms = matchSection(line)
        if ms:
            indent  = ms.group(1)
            heading = ms.group(2)
            page    = offset + int(ms.group(3))
            yamlText += f'''\
{indent}-
{indent} heading: {heading}
{indent} page: {page}
{indent} children:
'''
            continue

        raise ValueError(f"Syntax error at line {linenum} in the bkm file: {line}")
    return yamlText

