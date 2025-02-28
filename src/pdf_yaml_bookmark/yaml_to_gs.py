import yaml

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
        heading     = section["heading"]
        children    = section["children"] or []
        count       = len(children)
        gsList.append(f"[/Page {page} /View [/XYZ null null null] /Title <{fmt_gs_string(heading)}> /Count {count} /OUT pdfmark")
        traverse_sections(children, gsList)

def yaml_to_gs(yamlText):
    sections = yaml.safe_load(yamlText) or []
    gsList = []
    traverse_sections(sections,gsList)
    return '\n'.join(gsList)
