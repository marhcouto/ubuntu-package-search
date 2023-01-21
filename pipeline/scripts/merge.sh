#!/bin/bash

output_file=package_data/csv_res/clean/all.csv

cp package_data/csv_res/clean/universe.csv $output_file &&
tail -n +2 package_data/csv_res/clean/main.csv >> $output_file &&
tail -n +2 package_data/csv_res/clean/restricted.csv >> $output_file &&
tail -n +2 package_data/csv_res/clean/multiverse.csv >> $output_file
