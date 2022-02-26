import pickle
import os
import shutil
import numpy as np
from reads_task_dat import readFile
from smt.surrogate_models import RBF, KPLS, KPLSK, KRG


def training_function(ndoe, n, nbeta, beta, F, nc):
    #----------------One metamodel for every objective-----------------------
    #
    #-------------------Train RBF-----------------------
    #rootfolder = '/gpuhome/gpuopt06/n4318_off_line/optim_cruise/metamodel_cache/obj_fun_model'
    #funtemp = 'obj{0}'
    #for j in range(n):
    #    mydir_fun_sep = rootfolder + '/' + funtemp.format(str(j))
    #    if os.path.exists(mydir_fun_sep): 
    #        shutil.rmtree(mydir_fun_sep)  #remove old directory
        
    #    os.mkdir(mydir_fun_sep)
       
    #    fun_model = RBF(d0 = 80, poly_degree = 1, data_dir =  mydir_fun_sep, print_global = False)
    #    fun_model.set_training_values(beta, F[:,j])
    #    fun_modet( 
    #-----------------------------------------------------

    #----------------Train KRG, KPLS, KPLSK---------------
    print(beta)
    fun_temp = 'obj{0}.pickle'
    n_com = 3
    th_range = np.array([1e-8, 1e+3])
    for j in range(n):
        fun_model = KPLS(n_comp = n_com, theta0 = [1e-2]*n_com, theta_bounds = th_range, poly = 'constant', corr = 'squar_exp', print_global = False)
        fun_model.set_training_values(beta,F[:,j])
        fun_model.train()

        #-------Save the trained metamodel
        with open(fun_temp.format(str(j)), 'wb') as save_fun:
            pickle.dump(fun_model, save_fun, protocol = -1)
    #-----------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------

    #-----------------------------Metamodel for constraints -----------------------------------
    if nc != 0:
        skip = 0
        con = readFile('con.dat', skip)
        nlen = con.shape[0]
        con = con.reshape(nlen, nc)
        #----------------One metamodel for every constraint-----------------------
        #
        #-------------------Train RBF-----------------------
        #rootfolder = '/gpuhome/gpuopt06/n4318_off_line/optim_cruise/metamodel_cache/con_model'
        #contemp = 'con{0}'
        #for j in range(nc):
        #    mydir_con_sep = rootfolder + '/' + contemp.format(str(j))
        #    if os.path.exists(mydir_con_sep): 
        #        shutil.rmtree(mydir_con_sep)  #remove old directory

        #    os.mkdir(mydir_con_sep)

        #    con_model = RBF(d0 = 100, poly_degree = 1, data_dir =  mydir_con_sep, print_global = Fal
        #    con_model.set_training_values(beta, con[:,j])
        #    con_model.train()
        #-----------------------------------------------------

        #----------------Train KRG, KPLS, KPLSK---------------
        pickletemp = 'constraint{0}.pickle'
        #polynom = ['quadratic', 'quadratic', 'constant', 'quadratic', 'constant']
        #correlation = ['abs_exp', 'matern52', 'squar_exp', 'matern52', 'squar_exp']
        th_range = np.array([1e-8, 1e+3])
        n_com = 3
        for j in range(nc):
            con_model = KPLS(n_comp = n_com, theta0 = [1e-2]*n_com, theta_bounds = th_range, poly = 'constant', corr = 'squar_exp', print_global = False)
           #con_model = KRG(theta0 = [1e-2]*nbeta, theta_bounds = th_range, poly = polynom[j], corr = correlation[j], print_global = False)
            con_model.set_training_values(beta,con[:,j])
            con_model.train()

            #-------Save the trained metamodel
            with open(pickletemp.format(str(j)), 'wb') as save_con:
                pickle.dump(con_model, save_con, protocol = -1)
        #-----------------------------------------------------
        #--------------------------------------------------------------------------
        #
        #
        #
        #-------------One metamodel for all constraint----------------------------
        #
        #----------Load KRG, KPLS, KPLSK-------
        #n_com = 2
        #th_range = np.array([1e-10, 1e+3])
        #con_model = KPLS(n_comp = n_com, theta0 = [1e-2]*n_com, theta_bounds = th_range, poly = 'qua
        #con_model.set_training_values(beta,con)
        #con_model.train()

        #------Save trained surrogate model-----
        #with open('con_model.pickle', 'wb') as saved:
        #    pickle.dump(con_model, saved)
        #--------------------------------------

        #---------------Train RBF--------------
        #mydir_con_all = '/gpuhome/gpuopt06/n4318_off_line/optim_cruise/metamodel_cache/con_model'
        #for f in os.listdir(mydir_con_all):
        #    if f.endswith(".dat"):
        #        os.remove(os.path.join(mydir_con_all, f))
    
        #create file from the new run
        #con_model = RBF(d0 = 80, poly_degree = 1, data_dir = mydir_con_all, print_global = False)
        #con_model.set_training_values(beta,con)
        #con_model.train()
        #-------------------------------------- 
