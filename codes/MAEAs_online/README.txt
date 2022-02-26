####The following Python scripts are made to run on the cluster of the PCOPT/NTUA with user profile gpuopt06
#as seen in the absolute path found in the scripts.
#The results refer to the case of optimization of NACA 4318 in cruise conditions 
#MAEAs with on-line trained external metamodels are used

1) optSMT_online.easy is the EASY executable, where the parameters of the optimization can be found
2) reads_task_dat.py reads the task.dat file that EASY writes
3) read_metadb.py reads the training patterns selected by EASY
4) sciptSMT_online.bat performs the evaluation on the PSM
5) train.py performs the training of the metamodel
6) prediction.py performs the prediction using the trained metamodel
