####The following Python scripts are made to run on the cluster of the PCOPT/NTUA with user profile gpuopt06
#as seen in the absolute path found in the scripts.
#The results refer to the case of optimization of NACA 4318 in cruise conditions


1) offline_n4318.py is the Pthon script responsible for sychronising all the subprocesses
2) opt_offline.easy is the EASY executable, where the parameters of the optimization can be found
3) read_column.py reads some column of a matrix
4) read_out_L1.py reads the optimal solution found in out_L1.log file that EASY writes
5) reads_task_dat.py reads the task.dat file that EASY writes
6) read_trainin_patterns.py reads the necessary training patterns
7) sampling_code1,py performs the sampling with the use of a DoE technique
8) model_values_code2.py performs the evaluation on the PSM
9) training_code3.py performs the training of the metamodel
10) elite_evaluation.py reads the elite/s and re-evaluates them on the PSM, while calculating the deviation of the results
11) preprocessor.py performs the prediction using the trained metamodel
