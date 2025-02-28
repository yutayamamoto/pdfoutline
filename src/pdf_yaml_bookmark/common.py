import os
import sys

def eprint(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)

def check_readability(path):
    if not os.path.exists(path):
        eprint('{}: not found'.format(path))
        return False
    if not os.access(path, os.R_OK):
        eprint('{}: not readable'.format(path))
        return False
    return True
