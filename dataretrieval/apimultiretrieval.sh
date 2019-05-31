#!/bin/bash

# make the temporary and output directories if necessary
mkdir -p temp output
# remove contents of temporary directory used to stash output csvs before concatenations
rm -rf temp/*

# assign the string variables
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -s|--states)
    statesStr="$2"
    shift # past argument
    shift # past value
    ;;
    -y|--years)
    yearsStr="$2"
    shift # past argument
    shift # past value
    ;;
    -fn|--filename)
    outFilename="$2"
    shift # past argument
    shift # past value
    ;;
esac
done

# Set the internal field seperator
IFS=','

# assign arrays
read -ra statesArr <<< "$statesStr"
read -ra yearsArr <<< "$yearsStr"

# generate files in ./temp and push them to data.world
for i in "${!statesArr[@]}"; do
    for j in "${!yearsArr[@]}"; do
        if [ $i -eq 0 ] && [ $j -eq 0 ]
        then
            python dataretrieval.py ${statesArr[$i]} ${yearsArr[$j]} --dest api --isfirst
        else
            python dataretrieval.py ${statesArr[$i]} ${yearsArr[$j]} --dest api
        fi
    done
done

unset IFS

# remove the temp dir
rm -rf temp/
