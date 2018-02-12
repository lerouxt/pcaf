#!/usr/bin/env python3

import pandas
import logging
import argparse
import numpy as np

logging.basicConfig(level=logging.INFO)

def to_xls(infile1, infile2, outfile):

    df1 = pandas.read_csv(infile1)
    df2 = pandas.read_csv(infile2)

    wtr = pandas.ExcelWriter(outfile)
    df1.to_excel(wtr, 'AllData', index=False)
    df2.to_excel(wtr, 'Flattened', index=False)
    wtr.save()

def main():
    parser = argparse.ArgumentParser(description='Process form data')
    parser.add_argument('--infile1', help='File for first XLS tab')
    parser.add_argument('--infile2', help='File for second XLS tab')
    parser.add_argument('--outfile', help='Name of XLS file to write')

    args = parser.parse_args()

    to_xls(args.infile1, args.infile2, args.outfile)

main()
