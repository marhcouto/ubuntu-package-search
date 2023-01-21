#!/bin/bash

grep 'Package: ' out/raw_data/universe_packages.txt | sed 's/Package: //' > out/package_lists/universe_packages_names.txt
grep 'Package: ' out/raw_data/main_packages.txt | sed 's/Package: //' > out/package_lists/main_packages_names.txt
grep 'Package: ' out/raw_data/multiverse_packages.txt | sed 's/Package: //' > out/package_lists/multiverse_packages_names.txt
grep 'Package: ' out/raw_data/restricted_packages.txt | sed 's/Package: //' > out/package_lists/restricted_packages_names.txt
