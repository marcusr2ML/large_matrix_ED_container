#!/bin/bash

# This script is meant to be EXEC'd by the container.
# These are the guts of the original Job_solve.sbash

PROJ=~/scratch/

cd $PROJ/paral_new

PHYSDIR=$PWD
SRC=solver-cpp
RUNDIR=$PHYSDIR/$1

cd $PHYSDIR/$SRC
echo $PWD
git pull
./compile_solve.sh $2 2>&1 | tee build/compile_output_solve.txt


mkdir -p $RUNDIR
cp $PHYSDIR/$SRC/build/solve $RUNDIR/
cd $RUNDIR 
stdbuf --output=L ../launch_solve.sh 2>&1 | tee solve.log
