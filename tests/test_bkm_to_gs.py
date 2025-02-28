import unittest


import pdf_yaml_bookmark.bkm_to_gs as bg

sample_bkm = '''\
# this is a comment
First Chapter 1
    First section 1
        Second section 1
# - offset: 5
First Chapter 1
    First section 1
    Second section 1\
'''

def fmt_gs_string(s):
    return "FEFF" + s.encode("utf-16-be").hex()
    # return s

sample_gs=f'''\
[/Page 1 /View [/XYZ null null null] /Title <{fmt_gs_string("First Chapter")}> /Count 1 /OUT pdfmark
[/Page 1 /View [/XYZ null null null] /Title <{fmt_gs_string("First section")}> /Count 1 /OUT pdfmark
[/Page 1 /View [/XYZ null null null] /Title <{fmt_gs_string("Second section")}> /Count 0 /OUT pdfmark
[/Page 1 /View [/XYZ null null null] /Title <{fmt_gs_string("First Chapter")}> /Count 2 /OUT pdfmark
[/Page 1 /View [/XYZ null null null] /Title <{fmt_gs_string("First section")}> /Count 0 /OUT pdfmark
[/Page 1 /View [/XYZ null null null] /Title <{fmt_gs_string("Second section")}> /Count 0 /OUT pdfmark\
'''


class TestBkmToGs(unittest.TestCase):
    def test_bkm_to_gs(self):
        gs_script = bg.elist_to_gs(bg.toc_to_elist(sample_bkm, ""))
        self.assertEqual(gs_script, sample_gs)

