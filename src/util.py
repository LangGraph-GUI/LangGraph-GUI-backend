# util.py

import sys
import os

def logger(*args, **kwargs):
    output = ""
    for arg in args:
      output += str(arg)
    
    output = output.replace("\n", "\\n")
    print(output, **kwargs)
    sys.stdout.flush()