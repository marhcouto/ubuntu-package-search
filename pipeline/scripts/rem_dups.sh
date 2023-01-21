#!/bin/bash

while getopts i:o: flag
do
    case "${flag}" in
        i) input_path=${OPTARG};;
        o) output_path=${OPTARG};;
    esac
done

if [ -z ${input_path} ];
then
    echo 'Please specify the input path with -i'
fi

if [ -z ${output_path} ];
then
    echo 'Please specify the output path with -o'
fi

if [ ! -z ${input_path} ] && [ ! -z ${output_path} ];
then
    printf '%s\n' $(head -1 ${input_path}) > ${output_path}
    tail -n +2 ${input_path} | sort | uniq -u >> ${output_path}
fi
