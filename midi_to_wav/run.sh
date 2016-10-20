#!/bin/bash
# example use: bash run.sh <$1> <$2> first parameter should be file directory of input file, second should be file directory of output files
# Must have timidity installed: brew install timidity
cnt=0
replace=parquet
makedir="mkdir $2"
for file in `ls $1`
do
newfile="$2/${file}.wav"
inst="timidity $0/$file -Ow -o $newfile"
echo $inst
((cnt++))
done
echo
exit