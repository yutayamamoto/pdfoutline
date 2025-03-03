import unittest

# Workaround
import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent) + "/src")

import pdf_yaml_bookmark.bkm_to_yaml as by

sample_bkm = '''\
# this is a comment
First Chapter 1
    First section 1
        Second section 1
+5
First Chapter 1
    First section 1
    Second section 1\
'''

sample_yaml = '''\
# this is a comment
-
 heading: First Chapter
 page: 1
 offset: 0
 children:
    -
     heading: First section
     page: 1
     offset: 0
     children:
        -
         heading: Second section
         page: 1
         offset: 0
         children:
-
 heading: First Chapter
 page: 1
 offset: 5
 children:
    -
     heading: First section
     page: 1
     offset: 5
     children:
    -
     heading: Second section
     page: 1
     offset: 5
     children:
'''

class TestBkmToYaml(unittest.TestCase):
    def test_bkm_to_yaml(self):
        self.assertEqual(by.bkm_to_yaml(sample_bkm), sample_yaml)

