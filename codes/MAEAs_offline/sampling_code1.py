import numpy as np
from smt.sampling_methods import LHS, Random, FullFactorial

def  sampling_function(ndoe, doe_new, n_cyc):
    #-----------------------Sampling-----------------------------
    #x1 = [0.125, 10.0], x2 = [0.1, 10.0], x3 = [0.1, 10.0], x4 = [0.1, 10.0] :welded beam
    # x1 = [0.25,1.3], x2 = [0.05, 2.0], x3 = [2.0, 15.0] :spring
    #x1 = [2.6, 3.6], x2 = [0.7, 0.8], x3 = [17.0, 28.0], x4 = [7.3, 8.3], x5 = [7.3, 8.3], x6 = [2.9, 3.9], x7 = [5.0, 5.5] :speed reducer

    #-----------------Perform DoE-------------------------------------
    #betalimits = np.array([[0.125, 10.0], [0.1, 10.0], [0.1, 10.0], [0.1, 10.0]]) #welded beam
    #betalimits = np.array([[0.25, 1.3], [0.05, 2.0], [2.0, 15.0]]) #spring 
    #betalimits = np.array([[2.6, 3.6], [0.7, 0.8], [17.0, 28.0], [7.3, 8.3], [7.3, 8.3], [2.9, 3.9], [5.0, 5.5]]) #speed reducer
    betalimits = np.array([[-0.26, -0.24], [-0.26, -0.24], [-0.26, -0.24], [-0.26, -0.24], [-0.26, -0.24], [-0.01, 0.01], [-0.01, 0.01], [-0.01, 0.01], [0.24, 0.26], [0.24, 0.26], [0.24, 0.26], [0.24, 0.26], [0.24, 0.26] ])
 
    if n_cyc == 0: 
        sampling = LHS(xlimits = betalimits, criterion = 'ese')   
        beta = sampling(ndoe)
    else:
        sampling = Random(xlimits = betalimits)   
        beta = sampling(doe_new)
    #------------------------------------------------------------------

    #---------------------Printing-------------------------------
    #Print sampling results -> task.dat
    np.savetxt('sample_points.dat', beta, fmt='%1.8f',delimiter = '   ' )
