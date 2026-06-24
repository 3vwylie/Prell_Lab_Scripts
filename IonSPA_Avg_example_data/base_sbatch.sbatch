#!/bin/bash
#SBATCH --partition=compute       ### queue to submit to
#SBATCH --job-name=STX11M   ### job name
#SBATCH --output=ionspa_out         ### file in which to store job stdout
#SBATCH --error=ionspa_err          ### file in which to store job stderr
#SBATCH --time=24:00:00        ### Wall clock time limit in HH:MM:SS
#SBATCH --constraint=amd,milan     ### Constrain to certain processor types
#SBATCH --nodes=1               ### number of nodes to use
#SBATCH --ntasks-per-node=28    ### nuimber of tasks to launch per node
#SBATCH --cpus-per-task=1       ### number of cores for each task
#SBATCH --mail-user=agreen8@uoregon.edu
#SBATCH --mail-type=begin  # email me when the job starts
#SBATCH --mail-type=end    # email me when the job finishes
#SBATCH --mail-type=fail    # email me when the job finishes
#SBATCH --account=prell_lab      ### Account used for job submission
#SBATCH --mem=48G
module purge
module load miniconda3
conda activate mpi_python-250414
