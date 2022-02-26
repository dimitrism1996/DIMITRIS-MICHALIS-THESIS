#!/usr/bin/env python3

import numpy as np
import pickle
import os
import shutil
from read_metadb import meta_db
from smt.surrogate_models import KPLS, KRG, KPLSK, RBF

#-------------------------Read meta.db--------------------------
ncon = 0 #number of constraints
nt, nbeta, n, beta, F = meta_db()
#----------------------------------------------------------------
#
#-----------------------Training of the model for the objective function-------------------------
#----------------One metamodel for every constraint-----------------------
#
#-------------------Train RBF-----------------------
#rootfolder = '/gpuhome/gpuopt06/n4318_SMT_on_line/optim2/metamodel_cache/obj_fun_model'
#funtemp = 'obj{0}'
#for j in range(n):
#    mydir_fun_sep = rootfolder + '/' + funtemp.format(str(j))
#    if os.path.exists(mydir_fun_sep): 
#        shutil.rmtree(mydir_fun_sep)  #remove old directory
    
#    os.mkdir(mydir_fun_sep)
   
#    fun_model = RBF(d0 = 100, poly_degree = 1, data_dir =  mydir_fun_sep, print_global = False)
#    fun_model.set_training_values(beta, F[:,j])
#    fun_model.train()
#-----------------------------------------------------

#----------------Train KRG, KPLS, KPLSK---------------
fun_temp = 'obj{0}.pickle'
n_com = 3
th_range = np.array([1e-8, 1e+3])
for j in range(n):
    #fun_model = KRG(theta0 = [1e-2]*nbeta, theta_bounds = th_range, poly = 'quadratic', corr = 'squar_exp', print_global = False)
    fun_model = KPLS(n_comp = n_com, theta0 = [1e-2]*n_com, theta_bounds = th_range, poly = 'constant', corr = 'squar_exp', print_global = False)
    fun_model.set_training_values(beta,F[:,j])
    fun_model.train()

    #-------Save the trained metamodel
    with open(fun_temp.format(str(j)), 'wb') as save_fun:
        pickle.dump(fun_model, save_fun, protocol = -1)
#-----------------------------------------------------

