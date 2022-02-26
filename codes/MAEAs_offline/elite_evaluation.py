import numpy as np
import subprocess
from reads_task_dat import readFile
from read_out_L1 import read_pred_elites


def eval_elites(ndoe, n, nbeta, nc):
    #------------------Reads λe elites------------------------------- 
    if nc == 0:
        el, Felpred = read_pred_elites(ndoe, n, nbeta, nc)
    else:    
        el, Felpred, conelpred = read_pred_elites(ndoe, n, nbeta, nc) 

    nel = el.shape[0] #number of elites selected for evaluation
    #--------------------------------------------------------------

    e = np.zeros((nel,n))
    ec = np.zeros( (nel,nc) )
    if nel == 0:
        fl = True 
        return fl, nel, e, ec
    else:    
        #----------------Find f values in the sampling points------------
        #the define_F function includes F, so we have ndoe number of iterations
        #the function.py scripts replaces the CFD.exe (task.bat)
        Fel = np.zeros((nel,n))
        if nc != 0:
            conel = np.zeros((nel, nc))
       
        for i in range(nel):
            #Prind ind.dat for each elite that needs to be evaluated on the PSM
            with open('task.dat', 'w+') as f:
                f.write(str(nbeta))
                f.write('\n')
                for j in range(nbeta):
                    f.write( str(el[i,j]) )
                    f.write('\n')
            #-------------------------------------------------------------------
            subprocess.run('/gpuhome/gpuopt06/n4318_off_line/optim_cruise/script_eval.bat')
            skip = 0
            Fel[i,:] = readFile('task.res', skip)
            #--------------------Constraint evaluation---------------------
            if nc != 0:
                conel[i,:] = readFile('task.cns', skip)
            #------------------------------------------------------------------        
        #---------------Creates the model_valus file-----------------------
        #the task.res file is the input for EASY
        elite_values = np.zeros((nel, nbeta+n+nc))
        elite_values = np.hstack((el, Fel))
        
        if nc != 0:  
            elite_values = np.hstack((elite_values, conel))

        elite_valuesDAT = np.savetxt('out.log',  elite_values, fmt='%1.8f',delimiter = '    ')
        #----------------------------------------------------------------------

        #----------------Calculate accuracy-------------------------------------
        for i in range(nel):
            for j in range(n):
                e[i,j] = abs((Fel[i,j] - Felpred[i,j])/Fel[i,j])
   
                if all(e[i,:] < 10**(-2)):
                    fl1 = False
                    fl = False
                else:
                    fl1 = True
                    fl = True

        if nc == 0:        
            return fl, nel, e, ec              
        else:
            for i in range(nel):
                for j in range(nc):
                    ec[i,j] = abs((conel[i,j] - conelpred[i,j])/conel[i,j])
                    
                if all(ec[i,:] < 0.5):
                    fl2 = False 
                else: 
                    fl2 = True
        
            fl = fl1 or fl2 
        
            return fl, nel, e, ec
