import sys
import yaml

import pdf_yaml_bookmark.common as common

def fmt_gs_string(s):
    return "FEFF" + s.encode("utf-16-be").hex()

def traverse_sections(sections, gsList):
    """
    Recursively traverses `sections`, translate them into list of ghostscript
    codes, append them to `gsList`.
    `gsList` is a list of strings.
    `sections` is a YAML object that has the structure of a list of "sections,"
    i.e., a list of {"title": str, "page": int, "children": [ section ]}.
    """
    for section in sections:
        page        = section["page"]
        offset      = section["offset"]
        heading     = section["heading"]
        children    = section["children"] or []
        count       = len(children)
        gsList.append(f"[/Page {page+offset} /View [/XYZ null null null] /Title <{fmt_gs_string(heading)}> /Count {count} /OUT pdfmark")
        traverse_sections(children, gsList)

# TODO: printing syntax errors for YAML appropriately
def yaml_to_gs(yamlText):
    sections = yaml.safe_load(yamlText) or []
    gsList = []
    try:
        traverse_sections(sections,gsList)
    except TypeError:
        common.eprint('Syntax error in YAML file.')
        sys.exit(-1)
    return '\n'.join(gsList)
