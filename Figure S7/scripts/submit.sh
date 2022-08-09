#!/bin/bash -l

#$ -l h_rt=24:00:0
#$ -l mem=5G
#$ -l tmpfs=10G
#$ -t 1-1280
#$ -N K_sigma
#$ -wd /home/ucabpod/Scratch/gopgar/K_sigma/logs

module load python3/recommended
source /home/ucabpod/Genetic-Evolution-in-OPGG/env/bin/activate

number=${SGE_TASK_ID}
paramfile=/home/ucabpod/Scratch/gopgar/K_sigma/scripts/K_parameters.txt

index="`sed -n ${number}p $paramfile | awk '{print $1}'`"
p="`sed -n ${number}p $paramfile | awk '{print $2}'`"
sigma="`sed -n ${number}p $paramfile | awk '{print $3}'`"
norm="`sed -n ${number}p $paramfile | awk '{print $4}'`"

cd ${TMPDIR}
python /home/ucabpod/Scratch/gopgar/K_sigma/scripts/run.py ${index} ${p} ${sigma} ${norm}
tar zcvf /home/ucabpod/Scratch/gopgar/K_sigma/raw_data/${index}.tar.gz ${TMPDIR}
