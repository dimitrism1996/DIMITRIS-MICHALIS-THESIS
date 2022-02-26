import numpy as np
from reads_task_dat import checkFile


def read_col(fname, col, skip_lines, sep=None):
    """Read text files with columns separated by `sep`.

    fname - file name
    col - index of column to read
    convert - function to convert column entry with
    sep - column separator
    If sep is not specified or is None, any
    whitespace string is a separator and empty strings are
    removed from the result.
    """
    checkFile(fname)
    
    with open(fname,'r') as fobj:
        # skip first `skip_lines` lines
        for _ in range(skip_lines):
            next(fobj)

        res = []
        for line in fobj:
            parts = line.split(sep=sep)
            if len(parts) > 1:
                res.append(parts[col])
                  
    return res