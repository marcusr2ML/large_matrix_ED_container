#! /bin/sh

EXECDIR=$PWD

EXEC="solve"
N=360
ITV="intervals.txt"
K=650
XTOL=2500

./$EXEC $N $ITV $K $XTOL
