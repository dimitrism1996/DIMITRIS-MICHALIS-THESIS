import sys
import os
import numpy as np

def checkFile(fname):
      if not os.path.exists(fname):
            print ('# File',fname,'does not exist')
            sys.exit(1)

def readFile(fname, skip_lines):
      with open(fname,'r') as fobj:
            # skip first `skip_lines` lines
            for _ in range(skip_lines):
                  next(fobj)
            x=[]
            checkFile(fname)
            x = np.loadtxt(fobj)

      return x