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

# generate files in ./temp
for i in "${statesArr[@]}"; do
    for j in "${yearsArr[@]}"; do
        python dataretrieval.py $i $j --outdir ./temp
    done
done

unset IFS

outputFile () {
    i=0
    output_file="./output/""$1"".csv"
    files=$(ls "./temp/""$1"*".csv")
    for filename in $files; do
        if [[ $i -eq 0 ]] ; then
            # copy csv headers from first file
            head -1 $filename > $output_file
        fi
        # copy csv without headers from other files
        tail -n +2 $filename >> $output_file
        i=$(( $i + 1 ))
    done
}

outputFile "incidents"
outputFile "offenders"
outputFile "offenses"
outputFile "victims"
outputFile "arrestees"

rm -rf temp/
