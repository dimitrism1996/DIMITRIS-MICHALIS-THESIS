#!/usr/bin/env python3

import numpy as np
import pickle
from reads_task_dat import readFile
from smt.surrogate_models import RBF
#from function import calc_F

#-----------------Initialize n, nc-------------------------
nbeta, n, ncon = 13, 1, 1
#----------------------------------------------------
#
#-----------------Read task.dat----------------------- 
skip = 1
cand = readFile('task.dat', skip)
#-----------------------------------------------------------------
#
#-----------Load saved surrogate model for the objective function and predict its values---------------------
#------------RBF------------------- 
#skip = 0
#beta0 = readFile('beta.dat', skip)
#F0 = readFile('F.dat', skip)
Fpredict = np.zeros(n)
#
#--------------One metamodel for each objecive------------
#
#---------Load RBF---------------
#rootfolder = '/gpuhome/gpuopt06/n4318_off_line/optim_cruise/metamodel_cache/obj_fun_model'
#funtemp = 'obj{0}'
#for j in range(n):
#    mydir_fun_sep = rootfolder + '/' + funtemp.format(str(j))
#    fun_model = RBF(d0 = 80, poly_degree = 1, data_dir = mydir_fun_sep, print_global = False)
#    fun_model.set_training_values(beta0, F0[:,j])
#    fun_model.train()
#    fun_pred = fun_model.predict_values(cand.reshape(1,nbeta))
#    Fpredict[j] = fun_pred[0,0]
#--------------------------------
#    
#-----load KRG, KPLS, KPLSK-------
pic_fun_temp = 'obj{0}.pickle'
for j in range(n):
    with open(pic_fun_temp.format(str(j)), 'rb') as save_fun:
        fun_model = pickle.load(save_fun)
        fun_pred = fun_model.predict_values(cand.reshape(1,nbeta))
        Fpredict[j] = fun_pred[0,0]
#-----------------------------------
#
#-----------------Print objectives----------------
with open('task.res','w+') as res:
    for i in range(n):
        res.write(str(Fpredict[i]))
        res.write('\n')
#---------------------------------------------------    
#-------------------------------------------------------------------------------------------------------
#
#
#
#--------------------------Trained metamodel for constraints---------------------------------------
if ncon != 0:
    conpredict = np.zeros(ncon)
    #skip = 0
    #con0 = readFile('con.dat', skip)

    #--------------One metamodel for each constraint------------
    #
    #---------Load RBF---------------
    #rootfolder = '/gpuhome/gpuopt06/n4318_off_line/optim_cruise/metamodel_cache/con_model'
    #contemp = 'con{0}'
    #for j in range(ncon):
    #    mydir_con_sep = rootfolder + '/' + contemp.format(str(j))
    #    con_model = RBF(d0 = 80, poly_degree = 1, data_dir = mydir_con_sep, print_global = False)
    #    con_model.set_training_values(beta0, con0[:,j])
    #    con_model.train()
    #    pred = con_model.predict_values(cand.reshape(1,nbeta))
    #    conpredict[j] = pred[0,0]
    #--------------------------------
    #    
    #-----load KRG, KPLS, KPLSK-------
    pickletemp = 'constraint{0}.pickle'
    for j in range(ncon):
        with open(pickletemp.format(str(j)), 'rb') as save_con:
            con_model = pickle.load(save_con)
            con_pred = con_model.predict_values(cand.reshape(1,nbeta))
            conpredict[j] = con_pred[0,0]
    #---------------------------------
    #
    #----------Print constraints-----
    with open('task.cns','w+') as cns:
        for j in range(ncon):
            cns.write(str(conpredict[j]))
            cns.write('\n')
    #------------------------------------------------------------- 
    #
    #---------------One metamodel for all constraints-------------
    #
    #-------load KRG, KPLS, KPLSK-----   
    #with open('con_model.pickle', 'rb') as con_saved:
    #    con_model = pickle.load(con_saved) 
    #----------------------------------
    #
    #---------load RBF-----------------
    #mydir_con_all = '/gpuhome/gpuopt06/n4318_off_line/optim_cruise/metamodel_cache/con_model'
    #con_model = RBF(d0 = 80, poly_degree = 1, data_dir = mydir_con_all, print_global = False)   
    #con_model.set_training_values(beta0, con0)
    #con_model.train()
    #---------------------------------
    #
    #---------Predict values----------
    #con_pred = con_model.predict_values(cand.reshape(1,nbeta))
    #----------------------------------
    #
    #---------Print constraints--------
    #with open('task.cns','w+') as cns:
    #    for j in range(ncon):
    #        cns.write(str(con_pred[0,j]))
    #        cns.write('\n')
    #------------------------------------        
#-------------------------------------------------------------------------------------------------
