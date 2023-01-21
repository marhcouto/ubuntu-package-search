#!/usr/bin/env python3

import csv
import subprocess
import sys

FIELDS = [ 'Package', 'Version', 'Section', 'Installed-Size', 'Essential', 
        'Depends', 'Pre-Depends', 'Recommends', 'Suggests', 'Breaks', 'Conflicts', 'Replaces', 'Description' ]
LIST_FIELDS = ['Depends', 'Pre-Depends', 'Recommends', 'Suggests', 'Breaks', 'Conflicts', 'Replaces']

def parser(package_data):

    fields_to_parse = set(FIELDS)
    list_fields = set(LIST_FIELDS)
    property_dict = {x: '' for x in FIELDS }
    lines = package_data.split("\n")
    should_include = False
    cur_field = ""

    for line in lines:
        if (len(line) != 0 and line[0] != ' '):
            sep_position = line.find(':')
            type_content = (line[0:sep_position], line[sep_position + 1:])
            cur_field = type_content[0]
            if (cur_field in fields_to_parse):
                should_include = True
                property_dict[cur_field] = type_content[1].strip()
            else:
                should_include = False
        elif should_include:
            property_dict[cur_field] += '\\n' + line[1:]

    for list_field in list_fields.intersection(fields_to_parse):
        if list_field in property_dict and property_dict[list_field] != '':
            property_dict[list_field] = [x for x in map(lambda x: x.strip(), property_dict[list_field].split(','))]

    return list(property_dict.values())


def get_data(package):

    package = package.replace('\n','')

    cmd = 'aptitude'
    output = []
    temp = subprocess.Popen([cmd,'show',package],stdout=subprocess.PIPE)
    output = (temp.communicate())
    
    return parser(output[0].decode())


def main():

    new_file = False
    usage = "python to_csv.py <path_to_package_names_file> <path_to_new_file> <file_opening_mode>(w or a)"
    
    # Detecting correct number of options
    if len(sys.argv) <= 1:
        print("Error: missing package name file location.")
        print("USAGE:", usage)
        exit(1)
    elif len(sys.argv) <= 2:
        print("Error: missing destination file.")
        print("USAGE:", usage)
        exit(1)
    elif len(sys.argv) <= 3:
        print("Error: missing file mode.")
        print("USAGE:", usage)
        exit(1)


    # Detecting valid file mode
    if (sys.argv[3] == 'w'):
        new_file = True
    elif (sys.argv[3] == 'a'):
        new_file = False
    else:
        print("Error: invalid file mode {}.".format(sys.argv[3]))
        exit(1)

    with open(sys.argv[1], 'r') as names_file, open(sys.argv[2], sys.argv[3]) as data_list:

        writer = csv.writer(data_list)

        if new_file:
            writer.writerow(FIELDS)

        num_packages = 0
        for line in names_file:
            data = get_data(line)
            if(data):
                writer.writerow(data)
                print(num_packages)
                num_packages += 1

if __name__ == "__main__":
    main()