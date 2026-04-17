#!/bin/bash

# Usage: ./Queue_solve_Jobs.sh 3 4 7

for i in "$@"; do
    echo "sbatch Job_solve_${i}.sbatch fac-interval${i} double"
    sbatch MVM_Job_solve_${i}.sbatch fac-interval${i} double
done
