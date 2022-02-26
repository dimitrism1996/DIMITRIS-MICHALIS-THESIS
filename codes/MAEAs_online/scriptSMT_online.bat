#! /bin/sh
source /etc/bashrc
source /gpuhome/gpuopt06/.bashrc

# Erase files from previous runs 
rm n4318* mada.* flow.*
rm AIRFOIL_BOX* slv0
rm ../mesh/*nod

# Get evaluation ID from task.id file
evalID=$(cat "task.id")

# Create task.dat required for mesh adaptation
mv task.dat ea.dat
head -1 ea.dat | awk '{print 2*$1}' >  task.dat
tail --lines=+2 ea.dat		    >> task.dat
tail --lines=+2 ea.dat		    >> task.dat

echo "-- Evaluation ${evalID} --" >> allTaskDat
cat task.dat >> allTaskDat

# Adapt mesh
../pumaG67_SMT_online.exe -i ada.ini >mada.out 2>mada.err
mv n4318_ADAPTED_BINARY.nod ../mesh/n4318_BINARY.nod

# Run CFD
../pumaG67_SMT_online.exe -d 0       >flow.out 2>flow.err

# Collect Results (objectives/constraints) 
tail -1 n4318.post | awk '{print -$26}' >  task.res
tail -1 n4318.post | awk '{print  $25}' >  task.cns

echo "-- Evaluation ${evalID} --" >> allTaskRes
cat task.res >> allTaskRes

echo "-- Evaluation ${evalID} --" >> allTaskCns
cat task.cns >> allTaskCns

