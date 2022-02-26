import os
import numpy as np
from reads_task_dat import readFile
from read_column import read_col

def read_pred_elites(ndoe0, n0, nbeta0, nc0):
    #------------------Read out_L1.log----------------------------------
    #-----read ndoe+n+nbeta+nc+1, where 1 is the number----
    #-----of columns that show system evaluation id------
    elite = 'out_L1.log'
    skip = 8 #skip 8 rows
    column = 0
    info = read_col(elite, column, skip, sep=None) #find nel
    nel0 = len(info)
    ntot = n0+nbeta0+nc0+1
    Felpred0 = np.zeros((nel0,n0))
    el0 = np.zeros((nel0,nbeta0))

    for j in range(ntot):
        column = j
        info = read_col(elite, column, skip, sep=None) 
        for i in range(nel0):
            if j < n0:   #read F(Pe)
                Felpred0[i,j] = info[i]  #row
            elif j >= n0+1 and j < n0+1+nbeta0:   #read elites 
                el0[i,j-n0-1] = info[i]  
    #-------------------------------------------------------------------

    if nc0 == 0:
        return el0, Felpred0
    else:   
        conelpred0 = np.zeros((nel0, nc0))
        for j in range(n0+1+nbeta0, ntot):
            column = j
            info = read_col(elite, column, skip, sep=None) 
            for i in range(nel0):
                conelpred0[i,j-n0-nbeta0-1] = info[i] 

        return  el0, Felpred0, conelpred0       
