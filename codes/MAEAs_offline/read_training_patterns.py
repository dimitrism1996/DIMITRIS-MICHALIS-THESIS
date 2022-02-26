import os
import numpy as np
from reads_task_dat import readFile
from read_column import read_col

def read_b_F(ndoe0, n0, nbeta0, nc0, nel0):
    #------------------Read mddel_values.dat------------------------------- 
    skip = 0
    values = readFile('model_values.dat', skip) 
    #--------------------------------------------------------------

    #seperate b,f in model_values.dat
    beta0 = np.zeros((ndoe0,nbeta0))
    for i in range(ndoe0):
        for j in range(nbeta0):
            beta0[i,j] = values[i,j]

    F0 = np.zeros((ndoe0,n0))
    for i in range(ndoe0):
        for j in range(n0):
            F0[i,j] = values[i,nbeta0+j]   
    #-------------------------------------------------------------------
            
    #------------------Read out.log----------------------------------
    #-----read ndoe+n+nbeta+1, where 1 is the number----
    #-----of columns that show system evaluation id------
    skip = 0
    elites = readFile('out.log', skip)
    el0 = np.zeros((nel0,nbeta0))
    Fel0 = np.zeros((nel0,n0))
    if nel0 == 1:
        for j in range(nbeta0):
            el0[0,j] = elites[j]

        for j in range(n0):
            Fel0[0,j] = elites[nbeta0+j] 
    else:    
        #seperate el,Felpred in out.log
        for i in range(nel0):
            for j in range(nbeta0):
                el0[i,j] = elites[i,j]

        for i in range(nel0):
            for j in range(n0):
                Fel0[i,j] = elites[i,nbeta0+j]    
        #-------------------------------------------------------------------

    if nc0 == 0:
        return beta0, F0, el0, Fel0
    else: #if there are constraints
        cn0 = np.zeros((ndoe0, nc0)) #values ftom model_values.dat
        for i in range(ndoe0):
            for j in range(nc0):
                cn0[i,j] = values[i, nbeta0+n0+j] 

        cnel0 = np.zeros((nel0,nc0)) #values from out.log
        if nel0 == 1:
            for j in range(nc0):
                cnel0[0,j] = elites[nbeta0+n0+j]        
        else:
            for i in range(nel0):    
                for j in range(nc0):
                    cnel0[i,j] = elites[i,nbeta0+n0+j]         

        return  beta0, F0, cn0, el0, Fel0, cnel0   
