import numpy as np
from reads_task_dat import readFile

def meta_db():

    with open('meta.db', 'r') as ini:
        first_line = ini.readline()
        part = first_line.split()
        nt1 = int(part[0])
        nbeta1 = int(part[1])
        n1 = int(part[2])      
    #-----------------------------------
    #
    #-------read β, F(β)---------------
    skip = 1
    values = readFile('meta.db', skip)
    beta1 = np.zeros((nt1,nbeta1))
    F1 = np.zeros((nt1,n1))

    for i in range(nt1):
        for j in range(nbeta1+n1):
            if j < nbeta1:
                beta1[i,j] = values[i,j]
            else:
                F1[i,j-nbeta1] = values[i,j] 

                
    return nt1, nbeta1, n1, beta1, F1