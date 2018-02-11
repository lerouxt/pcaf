#!/usr/bin/env python3

import pandas
import logging
import argparse
import numpy as np

logging.basicConfig(level=logging.INFO)

def to_xls(infile, outfile):

    df = pandas.read_csv(infile)

    wtr = pandas.ExcelWriter(outfile)
    df.to_excel(wtr, 'AllData')
    wtr.save()

def main():
    parser = argparse.ArgumentParser(description='Process form data')
    parser.add_argument('--infile', help='Name of pickled file of form data')
    parser.add_argument('--outfile', help='Name of XLS file to write')

    args = parser.parse_args()

    to_xls(args.infile, args.outfile)

main()
