#!/usr/bin/env python

import numpy as np
import pickle
from reads_task_dat import  readFile
from smt.surrogate_models import RBF
from read_metadb import meta_db

#----------Collect the same training patterns that were used for-------
#----------the training of RBF. These are found in meta.db and are-----
#----------used for the prediction phase based on RBF. pickle()-------
#----------requires no such process---------------------------------- 
#
#-------------------------Read meta.db--------------------------
ncon = 5 #number of constraints
nt, nbeta, n, beta0, F0 = meta_db()
#----------------------------------------------------------------                 
#
#
#-----------------Read meta.dat----------------------- 
skip = 1
cand = readFile('meta.dat', skip)
#-----------------------------------------------------------------
#
#-----------Load saved surrogate model for the objective function and predict its values---------------------
#------------RBF------------------- 
Fpredict = np.zeros(n)
#
#--------------One metamodel for each objecive------------
#
#---------Load RBF---------------
#rootfolder = '/gpuhome/gpuopt06/n4318_SMT_on_line/optim2/metamodel_cache/obj_fun_model'
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
with open('meta.res','w+') as res:
    for i in range(n):
        res.write(str(Fpredict[i]))
        res.write('\n')
#---------------------------------------------------    
