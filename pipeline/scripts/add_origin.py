#!/usr/bin/env python3

import argparse

def main():
    parser = argparse.ArgumentParser(description='Small script to add an origin to out csv')
    parser.add_argument('--in_file', type=str, help='The input path of csv file to clean')
    parser.add_argument('--out_file', type=str, help='The output path of the script')
    parser.add_argument('--origin', type=str, help='Original repo where the file came from')
    args = parser.parse_args()
    if args.in_file == None:
        print('Please provide a input file path')
    if args.out_file == None:
        print('Please provide a output file path')
    if args.origin == None:
        print('Please provide an origin')
    add_origin(args.in_file, args.out_file, args.origin)

def add_origin(input_file, output_file, origin):
    with open(input_file, 'r') as input:
        with open(output_file, 'w') as output:
            output.writelines(input.readline()[:-1] + ',Origin\n')
            for line in input:
                output.writelines(line[:-1] + ',' + origin + '\n')
            


if __name__ == '__main__':
    main()