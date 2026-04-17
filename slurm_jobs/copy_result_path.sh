#!/bin/bash

# Usage: ./copy_results <result dir> <# of intervals> <prefix>
# Example: ./copy_results ~/physics/results_n400 3 E_

printUsage() {
    echo 'Usage: ./copy_results <result directory name> <# of intervals> <prefix to copy>'
    echo 'Example: "./copy_results ~/physics/results_n400 3 E_" would create directories:'
    echo '         ~/physics/results_n400/0, ~/physics/results_n400/1, ~/physics/results_n400/2,'
    echo '         and copy the eigenvalues (files starting with "E_") to the corresponding result directories.'
    exit 1
}

re='^[0-9]+$'
if [[ $# != 3 ]] || ! [[ $2 =~ $re ]]; then
    printUsage
fi

RES_DNAME=$1   # full path to results directory (chosen by user)
N_ITV=$2       # number of intervals
PREFIX=$3      # file prefix to copy

# Make interval subdirectories inside the chosen results directory
for (( i=0; i<$N_ITV; i++ )); do
    echo "mkdir -p $RES_DNAME/$i"
    mkdir -p "$RES_DNAME/$i"
done

# Copy files with given prefix into the corresponding interval directories
for (( i=0; i<$N_ITV; i++ )); do
    echo "cp ./fac-interval$i/${PREFIX}* $RES_DNAME/$i/"
    cp ./fac-interval$i/${PREFIX}* "$RES_DNAME/$i/"
done
