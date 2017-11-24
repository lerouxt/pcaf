#!/usr/bin/env python3

import pandas
import logging
import argparse

logging.basicConfig(level=logging.INFO)

class Analyze():

    def __init__(self, infile=None):
        self.infile=infile

    def execute(self):
        df = pandas.read_pickle(self.infile)

        df2 = df.groupby('Sub-county')

        print(df2)

def main():
    parser = argparse.ArgumentParser(description='Process form data')
    parser.add_argument('--infile', help='Name of pickled file of form data')
    args = parser.parse_args()

    a = Analyze(infile=args.infile)
    a.execute()
    
main()
