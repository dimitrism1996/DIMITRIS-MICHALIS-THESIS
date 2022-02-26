#!/usr/bin/env python3

import sys
import os 
import numpy as np
from sampling_code1 import sampling_function
from model_values_code2 import model_values_function
from training_code3 import training_function
from reads_task_dat import readFile
from read_training_patterns import read_b_F
from elite_evaluation import eval_elites 

flag = True #starting cycle
cycle = int(0) 
ndoe1 = 80 #number of training points
nobj = 1 #number of onjectives
ndes = 13 #number of design variables
ncon = 1 #number of constraints

with open('init_pre.dat', 'w+') as send:
    send.write(str(ndes))
    send.write('\n')

    send.write(str(nobj))
    send.write('\n')

    send.write(str(ncon))
    send.write('\n')

ntotal = ndes+nobj+ncon
logTMP = 'run{0}.log' #out_L1.log file of cycle = 0
logT1 = 'out{0}.log' #out_L1.log file of cycle 0
#clear runs directory
clear1 = 'rm -r /gpuhome/gpuopt06/n4318_off_line/optim_cruise/runs/*'
os.system(clear1)
#------------------
nelite = [] #number of elites
nelite.append(0) # cycle 0 has 0 elites at the start of the algorithm 
non0cycle = [] #list of non zero cycles
ncycles = 15
extra_doe = 5
err_f = np.zeros((1,nobj))
err_con = np.zeros((1,ncon))

while flag and cycle < ncycles:
    #-----------------Sampling-----------------------------
    sampling_function(ndoe1, extra_doe, cycle) 
    #------------------------------------------------------

    #------------Exact evaluation of DoE--------------
    if cycle == 0:
        model_values1 = model_values_function(ndoe1, nobj, ndes, ncon)
        sum_values = model_values1
        np.savetxt('model_values.dat', sum_values, fmt='%1.8f',delimiter = '   ' )
    else:
        model_values1 = model_values_function(extra_doe, nobj, ndes, ncon)
        sum_values = np.vstack((sum_values, model_values1))
        np.savetxt('model_values.dat', sum_values, fmt='%1.8f',delimiter = '   ' ) 
    #------------------------------------------------------

    #----------------Read updated beta,F-------------------------------------
    #stack the elites that are read in each cycle
    #F1, Fel are evaluated using the exact model and consist the updated DB


    if nelite[cycle] == 0:  #if there is no elite, don't append
        #seperate b,f, con in values.dat
        beta1 = np.zeros((ndoe1,ndes))
        for i in range(ndoe1):
            for j in range(ndes):
                beta1[i,j] = sum_values[i,j]

        F1 = np.zeros((ndoe1,nobj))
        for i in range(ndoe1):
            for j in range(nobj):
                F1[i,j] = sum_values[i,ndes+j]

        if ncon != 0:
            cn1 = np.zeros((ndoe1, ncon))
            for i in range(ndoe1):
                for j in range(ncon):
                    cn1[i,j] = sum_values[i, ndes+nobj+j]

        if cycle == ncycles-1: #if the optimization returns an empty matrix during the last run
            beta1 = np.vstack((beta1, sumel))
            F1 = np.vstack((F1, sumFel))
            if ncon != 0:
                cn1 = np.vstack((cn1, sumcnel)) 
    else:
        if ncon == 0:
            beta1, F1, el1, Fel1 = read_b_F(ndoe1, nobj, ndes, ncon, nelite[cycle])
        else:    
            beta1, F1, cn1, el1, Fel1, cnel1 = read_b_F(ndoe1, nobj, ndes, ncon, nelite[cycle])
        #--------------    
        if cycle-1 == non0cycle[0]:
            sumel = el1
            sumFel = Fel1
            beta1 = np.vstack((beta1, sumel))
            F1 = np.vstack((F1, sumFel))
            if ncon != 0:
                sumcnel = cnel1
                cn1 = np.vstack((cn1, sumcnel))
        else:
            sumel = np.vstack((sumel, el1))
            sumFel = np.vstack((sumFel, Fel1))
            beta1 = np.vstack((beta1, sumel))
            F1 = np.vstack((F1, sumFel))
            if ncon != 0:
                sumcnel = np.vstack((sumcnel, cnel1))
                cn1 = np.vstack((cn1, sumcnel))
             
    betaDAT = np.savetxt('beta.dat', beta1, fmt='%1.8f',delimiter = '   ')
    FDAT = np.savetxt('F.dat', F1, fmt='%1.8f',delimiter = '   ')
    if ncon != 0:
        cnDAT = np.savetxt('con.dat', cn1, fmt='%1.8f',delimiter = '   ')
    #-------------------------------------------------------------------------

    #-------------Training of surrogate model--------------
    training_function(ndoe1, nobj, ndes, beta1, F1, ncon)
    #------------------------------------------------------
    
    #Copy L1_P1 file and use to initialize the optimization
    copy = 'cp /gpuhome/gpuopt06/n4318_off_line/optim/L1_P1 /gpuhome/gpuopt06/n4318_off_line/optim_cruise/'
    os.system(copy)
    rename = 'mv L1_P1 L1_P1.ini'
    os.system(rename)
    #-----------------------------------------------------

    #------------------Call EASY--------------------------
    #cmd = ['nohup', 'easy', 'eaConfig.easy', '>', 'ea.out', '2>', 'ea.err', '&']
    #subprocess.Popen(cmd).wait()
    runCom = 'easy opt_offline.easy'
    os.system(runCom)
    #----------------------------------------------------

    #------------Exact evaluation of elites--------------
    flag, new_el, e_fun, e_con = eval_elites(ndoe1, nobj, ndes, ncon)
    nelite.append(new_el) #create a list with elites: [0, nel[cycle=0], nel[cycle=1],..,nel[cycle=nfinal]]

    #print total errors
    if nelite[cycle+1] != 0:
        non0cycle.append(cycle) 
        if cycle == non0cycle[0]:  
            err_f = e_fun
            if ncon != 0:
                err_con = e_con
        else:
            err_f = np.vstack((err_f, e_fun))
            if ncon != 0:
                err_con = np.vstack((err_con, e_con))  
    #-------
    erFDAT = np.savetxt('error_f.dat', err_f, fmt='%1.8f',delimiter = '   ')
    if ncon != 0:
        erCONDAT = np.savetxt('error_con.dat', err_con, fmt='%1.8f',delimiter = '   ')
    #------------------------------------------------------

    #---------Print out_L1.log for current cycle-----------
    #create files
    logLoc = logTMP.format(str(cycle))
    mvCom = 'mv EA_L1.log ' + logLoc
    logloc1 = logT1.format(str(cycle))
    mvcom1 = 'mv out_L1.log ' + logloc1
    os.system(mvCom)
    os.system(mvcom1)
    #copy them to runs folder
    cpCom = 'cp ' + logLoc + ' /gpuhome/gpuopt06/n4318_off_line/optim_cruise/runs'
    cpcom1 = 'cp ' + logloc1 + ' /gpuhome/gpuopt06/n4318_off_line/optim_cruise/runs'
    os.system(cpCom)
    os.system(cpcom1)
    #delete files in main directory
    rmCom = 'rm ' + logLoc
    rmcom1 = 'rm ' + logloc1
    os.system(rmCom)
    os.system(rmcom1)
    #------------------------------------------------------
    
    cycle = cycle + 1
    ndoe1 = ndoe1 + extra_doe
#-----------------------------------------------------------------------------------------------------
#
#when the while loop closes, append the last value that it produced
ndoe_exit = ndoe1 - extra_doe
if cycle == ncycles or flag == False: 
    if ncon == 0:
        some_beta, some_F, el_last, Fel_last = read_b_F(ndoe_exit, nobj, ndes, ncon, nelite[cycle])
    else:    
        some_beta, some_F, some_cn, el_last, Fel_last, cnel_last = read_b_F(ndoe_exit, nobj, ndes, ncon, nelite[cycle])
        #print(cnel_last)
        cn1 = np.vstack((cn1, cnel_last))
        cnDAT = np.savetxt('con.dat', cn1, fmt='%1.8f',delimiter = '   ')

    beta1 = np.vstack((beta1, el_last))
    F1 = np.vstack((F1, Fel_last))
    betaDAT = np.savetxt('beta.dat', beta1, fmt='%1.8f',delimiter = '   ')
    FDAT = np.savetxt('F.dat', F1, fmt='%1.8f',delimiter = '   ')

#print number of selected elites in every cycle
with open('n_elites.dat', 'w+') as num:
    for i in range(cycle+1):
        num.write(str(nelite[i]))
        num.write('\n')
