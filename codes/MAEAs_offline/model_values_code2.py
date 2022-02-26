import numpy as np
import subprocess
from reads_task_dat import readFile

def model_values_function(ndoe, n, nbeta, nconstr):
    #------------------Reads sample_points.dat------------------------------- 
    sample_points = 'sample_points.dat'
    skip = 0
    beta = readFile(sample_points, skip)
    #--------------------------------------------------------------
    
    #----------------Exact evaluation of ndoe sample points-----------
    #the define_F function includes F, so we have ndoe number of iterations
    #the function.py scripts replaces the CFD.exe (task.bat)
    #print(beta[0,:].shape)
    F = np.zeros((ndoe,n))
    if nconstr != 0:
        con = np.zeros((ndoe, nconstr))

    for i in range(ndoe):
        #wite file ind.dat that will be used to solve the flow
        with open('task.dat', 'w+') as f:
            f.write(str(nbeta))
            f.write('\n')
            for j in range(nbeta):
                f.write( str(beta[i,j]) )
                f.write('\n')
        #---------------------------------------------------------

        subprocess.run('/gpuhome/gpuopt06/n4318_off_line/optim_cruise/script_eval.bat')
        F[i,:] = readFile('task.res', skip)  
        #--------------------Constraint evaluation-------------------------
        if nconstr != 0:
            con[i,:] = readFile('task.cns', skip)
        #-----------------------------------------------------------------

    #------------------Creates the model_va;ues.dat file-----------------
    model_values = np.hstack((beta, F))         
    if nconstr != 0:
        model_values = np.hstack((model_values, con))    
    #------------------------------------------------------------------    

    return model_values  
