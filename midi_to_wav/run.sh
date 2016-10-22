#!/bin/bash
# example use: bash run.sh <$1> <$2> first parameter should be file directory of input file, second should be file directory of output files
# Must have timidity installed: brew install timidity
makedir="mkdir $2"
eval $makedir
for file in `ls $1`
do
newfile="$2/${file}.wav"
inst="timidity $1/$file -Ow -o $newfile"
eval $inst
((cnt++))
done
echo
exit
