#!/bin/bash -l

#$ -l h_rt=72:00:0
#$ -l mem=5G
#$ -l tmpfs=10G
#$ -t 1-1920
#$ -N review_fig3_variable
#$ -wd /home/ucabpod/Scratch/gopgar/review_fig3/logs

module load python3/recommended
source /home/ucabpod/Genetic-Evolution-in-OPGG/env/bin/activate

number=${SGE_TASK_ID}
paramfile=/home/ucabpod/Scratch/gopgar/review_fig3/scripts/params.txt

index="`sed -n ${number}p ${paramfile} | awk '{print $1}'`"
n="`sed -n ${number}p ${paramfile} | awk '{print $2}'`"
p="`sed -n ${number}p ${paramfile} | awk '{print $3}'`"
norm="`sed -n ${number}p ${paramfile} | awk '{print $4}'`"

cd ${TMPDIR}
python /home/ucabpod/Scratch/gopgar/review_fig3/scripts/run_variable.py ${index} ${n} ${p} ${norm}
tar zcvf /home/ucabpod/Scratch/gopgar/review_fig3/raw_data/variable_${index}.tar.gz $TMPDIR
