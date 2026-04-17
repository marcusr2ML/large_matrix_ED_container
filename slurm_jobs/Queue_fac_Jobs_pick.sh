#!/bin/bash

# Usage: ./Queue_fac_Jobs.sh 3 4 7

for i in "$@"; do
    echo "Submitting: sbatch Job_fac.sbash interval${i}.txt double"
    sbatch Job_fac.sbash interval${i}.txt double
    sleep 0.5  # optional throttling to avoid hammering the scheduler
done
