# Complexity of behavioural strategies and cooperation in the Optional Public Goods Game

**Shirsendu Podder and Simone Righi**

s.podder@live.co.uk

This repository contains all of the code and data for each of the figures in the main paper as well as the supplementary materials. It consists of a number of `Figure x` directories as well as a `scripts` directory. The source code for the agent-based model is found in `Genetic-Evolution-in-OPGG`. 

The High Performance Computing system used (Myriad@UCL), outputs data in a potentially different format to other systems. Since Myriad uses a custom format, dissimilar to other HPC systems, this repository does not include the scripts to launch these simulations on a cluster. While the scripts given make it possible for the user to run single one-off simulations on their local machines, it is up to them to write their own submission scripts to any clusters. 

The authors acknowledge the use of the UCL Myriad High Performance Computing Facility (Myriad@UCL), and associated support services, in the completion of this work.

---

## General Experiment Procedure

The procedure that was followed for a single experiment (the output of which corresponds to a single Figure directory, `Figure S11` for example) is described here.

1. Create new experiment directory
2. Create `run.py` and `parameters.txt` setting up the simulations for the experiment. Suppose there are 10 unique values to explore under multiple norms. This would give 40 parameterisations for 1 repeat of the entire set of parameters. I found it helpful to repeat them in these 40 chunks, so the later scripts can be used incrementally and it would be possible to quickly visualise the patterns over the entire parameter range once just a few simulations had completed. 
3. Create `submit.sh` (not provided) to launch the experiment's simulations on a cluster, taking in the `run.py` and `parameters.txt` files. 
4. Simulate using an array job on Myriad@UCL.
5. Download partial results as compressed tarballs from cluster filesystem using `rsync` onto a fast SSD (I used a 2TB drive to store all the results). 
6. Extract them all into a different location on the external drive using `extract.py` which uses multiple cores to speed up the processing.
7. Summarise results with `summarise_actions.py` and save the output locally. For most cases, it is enough to get the level of cooperation/defection/abstention in the population. The extracted files were then deleted once the entire experiment has a full dataset summarised. 
8. Visualise the results. 
9. Repeat steps 5-8 as groups of simulations complete, periodically downloading the new data, and updating the summarised results and visualisations. 

---

## Figures Directories

Generally speaking, each figure directory will contain the following files. There may be some deviations, some experiments were not run at the same time so multiple versions of scripts may be present. 

### run.py & parameters.txt
This is a command line script to run a single simulation within an experiment. Default parameters are hardcoded, while the independent variables of the experiment are specified in `parameters.txt`. Each line in `parameters.txt` denotes a single simulation. The help documentation in `run.py` should explain the required inputs. 

To launch a large experiment in a cluster, a submission script needs to parse the `parameters.txt` file to assign each line of parameters to an individual job. 

### average_actions.csv
This is the output of the `scripts/summarise_actions.py` script which condenses the full dataset into a single file. Each simulation is averaged over the second half of the simulation only to get the overall level of cooperation, defection and abstention in the simulation. 

### plot.py
This is the script that uses the summarised dataset `average_actions.csv` and plots it. 

---

## Scripts Directory

There are four helper scripts that may be useful. These are all to be run from the command line. 

### extract.py

This is only useful if a HPC system is used that exports simulation results as a `.tar.gz` file. Then this command line script takes in the directory of tarballs (I called it `raw_data`), and extracts their data using multiple cores. This script notes and skips simulations that have not yet completed. It will skip simulations that have already been exported. Ideally, as results populate the local directory, this script is used occasionally. 

Upon running this script for the first time, a new directory `tmp` is made in the same directory as `raw_data`. All the config and csv files are outputted here. This is designed to be used just prior to `summarise_actions.py`. 

### summarise_actions.py

This command line script runs on the output of `extract.py`. It creates a single csv file with the summary results of C/D/L levels within the population. The `actions.csv` seen in each Figure directory are the outputs of this script. Once this script is used, the summary results are saved locally, while the raw tarballs are backed up on an external drive (SSD recommended) and the extracted data is deleted. This is because the extracted data can potentially be over 100GB. 

### find_duds.sh

Often simulations fail. This is a quick script to move all tarballs that are under a certain size into a separate directory for the user to confirm these simulations have failed, and then to easily delete. 

### get_param_file.py

This command line script was quickly thrown together to generate a parameter file. It became easier to create a new script for each experiment, so this was abandoned. It may still be useful, but equally may not work. 
