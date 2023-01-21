# Prepares filesystem
create_dir_tree:
	-mkdir -p out/package_lists/
	-mkdir -p out/csv_data/raw/
	-mkdir -p out/csv_data/clean/
	-mkdir -p out/raw_data/
	-mkdir -p out/analysis

give_exec_perm_to_scripts:
	chmod u+x scripts/add_origin.py
	chmod u+x scripts/data_analysis.py
	chmod u+x scripts/final_processing.py
	chmod u+x scripts/generate_lists.sh
	chmod u+x scripts/get_data.py
	chmod u+x scripts/merge.sh
	chmod u+x scripts/rem_dups.sh



# Collect phase
fetch_raw_package_lists:
	curl http://archive.ubuntu.com/ubuntu/dists/jammy/main/binary-amd64/Packages.xz --output out/raw_data/main_packages.xz
	curl http://archive.ubuntu.com/ubuntu/dists/jammy/multiverse/binary-amd64/Packages.xz --output out/raw_data/multiverse_packages.xz
	curl http://archive.ubuntu.com/ubuntu/dists/jammy/restricted/binary-amd64/Packages.xz --output out/raw_data/restricted_packages.xz
	curl http://archive.ubuntu.com/ubuntu/dists/jammy/universe/binary-amd64/Packages.xz --output out/raw_data/universe_packages.xz

	xz --stdout --decompress out/raw_data/main_packages.xz > out/raw_data/main_packages.txt
	xz --stdout --decompress out/raw_data/multiverse_packages.xz > out/raw_data/multiverse_packages.txt
	xz --stdout --decompress out/raw_data/restricted_packages.xz > out/raw_data/restricted_packages.txt
	xz --stdout --decompress out/raw_data/universe_packages.xz > out/raw_data/universe_packages.txt

	rm out/raw_data/*.xz

build_package_lists:
	scripts/generate_lists.sh

fetch_main_packages:
	scripts/get_data.py out/package_lists/main_packages_names.txt out/csv_data/raw/main.csv w

fetch_multiverse_packages:
	scripts/get_data.py out/package_lists/multiverse_packages_names.txt out/csv_data/raw/multiverse.csv w

fetch_restricted_packages:
	scripts/get_data.py out/package_lists/restricted_packages_names.txt out/csv_data/raw/restricted.csv w

fetch_universe_packages:
	scripts/get_data.py out/package_lists/universe_packages_names.txt out/csv_data/raw/universe.csv

fetch_packages: fetch_main_packages fetch_multiverse_packages fetch_restricted_packages fetch_universe_packages

fetch_ranking_signals:
	curl https://popcon.debian.org/by_inst.gz --output out/raw_data/pop-contest.gz
	gzip --stdout --decompress out/raw_data/pop-contest.gz > out/raw_data/pop-contest.txt
	rm out/raw_data/pop-contest.gz


# Process Phase
process_ranking_signals:
	sed '1,10d' out/raw_data/pop-contest.txt > out/csv_data/raw/pop-contest.txt
	sed -e 's/\s\+/,/g' out/csv_data/raw/pop-contest.txt > out/csv_data/raw/pop-contest.csv
	cut -d, -f2-7 out/csv_data/raw/pop-contest.csv > out/csv_data/clean/pop-contest.csv
	rm out/csv_data/raw/pop-contest.txt
	rm out/csv_data/raw/pop-contest.csv
	

remove_duplicates:
	scripts/rem_dups.sh -i out/csv_data/raw/main.csv -o out/csv_data/clean/main_no_dups.csv
	scripts/rem_dups.sh -i out/csv_data/raw/multiverse.csv -o out/csv_data/clean/multiverse_no_dups.csv
	scripts/rem_dups.sh -i out/csv_data/raw/restricted.csv -o out/csv_data/clean/restricted_no_dups.csv
	scripts/rem_dups.sh -i out/csv_data/raw/universe.csv -o out/csv_data/clean/universe_no_dups.csv

add_origin:
#	Adds a column to determine from which repo the package came
	scripts/add_origin.py --in_file out/csv_data/clean/main_no_dups.csv --out_file out/csv_data/clean/main.csv --origin main
	scripts/add_origin.py --in_file out/csv_data/clean/multiverse_no_dups.csv --out_file out/csv_data/clean/multiverse.csv --origin multiverse
	scripts/add_origin.py --in_file out/csv_data/clean/restricted_no_dups.csv --out_file out/csv_data/clean/restricted.csv --origin restricted
	scripts/add_origin.py --in_file out/csv_data/clean/universe_no_dups.csv --out_file out/csv_data/clean/universe.csv --origin universe

join_repos:
	cp out/csv_data/clean/main.csv out/csv_data/clean/all.csv
	tail -n +2 out/csv_data/clean/multiverse.csv >> out/csv_data/clean/all.csv
	tail -n +2 out/csv_data/clean/restricted.csv >> out/csv_data/clean/all.csv
	tail -n +2 out/csv_data/clean/universe.csv >> out/csv_data/clean/all.csv

final_processing:
# 	This script does the following tasks:
#	Removal of columns that only have null values,
# 	Adds a default value to the Essential column. According to Debian documentation the default value for this column is no.
#	Creates a column with the number of words of each description
	scripts/final_processing.py
	scripts/join_popularity_signals.csv


# Pipeline Targets
.PHONY: collect process analyse all
collect: fetch_raw_package_lists build_package_lists fetch_packages fetch_ranking_signals

process: process_ranking_signals remove_duplicates add_origin clean_no_dups join_repos final_processing clean_after_final_processing

analyse: 
	./scripts/data_analysis.py
	./scripts/check_pop-contest_coverage.py

all: create_dir_tree give_exec_perm_to_scripts collect process analyse



# Cleaning Targets
clean_collect:
	-rm -r out/raw_data
	-rm -r out/package_lists
	-rm -r out/csv_data/raw

clean_process:
	-rm -r out/csv_data/clean

clean_analyse:
	-rm -r out/analysis

clean_after_final_processing:
	rm out/csv_data/clean/all.csv

clean_no_dups:
	rm out/csv_data/clean/*_no_dups.csv

clean:
	rm -r out/
