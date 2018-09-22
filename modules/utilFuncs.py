'''Some file/path utility functions'''

import sys
import os

def findFileInSysPath(file):
    '''
    Tries to find the specified file in sys.path.
    Returns the original string if unsuccessful.
    '''
    for p in sys.path:
        path = os.path.join(p, file)
        if os.path.isfile(path):
            return path
    return file