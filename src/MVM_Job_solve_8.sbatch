#!/bin/bash
#SBATCH --job-name=container_test_slv
#SBATCH --time=04:00:00
#SBATCH --nodes=1
# SBATCH --gpus-per-node=2
#SBATCH --gres=gpu:1
# SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=16
# SBATCH --exclusive
# SBATCH --mem=0
#SBATCH --partition=IllinoisComputes-GPU
#SBATCH --account=marcusr2-ic
#SBATCH --mail-user=marcusr2@illinois.edu
#SBATCH --mail-type=BEGIN,END

# MVM for BASH debugging
set -x

# Useful info for top of output
echo $SLURM_JOB_NAME
whoami
hostname

PROJ=/u/marcusr2/scratch/marcusr2/	

# path to the container .sif file on campus cluster
SIF=$PROJ/paral_new/mycontainer_2.sif

# path to the solve script on campus cluster
# this is the guts from the original Job_solve.sh
PARALDIR=$PROJ/paral_new
SOLVE="$PARALDIR/mvm_solve.sh"
LUDIR="fac-interval8"
PRECISION=double

apptainer exec \
    --nv \
    --bind /scratch:/scratch \
    "$SIF" \
    "$SOLVE" $LUDIR $PRECISION
