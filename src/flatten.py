#!/usr/bin/env python3

import pandas
import logging
import argparse
import numpy as np

logging.basicConfig(level=logging.INFO)

def flatten(infile, outfile):

    df = pandas.read_csv(infile)

    right_cols = [ 'case_id', 'followup_visit', 'preipt_visit', 'phq9_9', 'phq9_total', 'psychoeducation_flag', 'functioning_total', 
                   'depressed_flag', 'severely_depressed_flag', 'suicidal_flag' ]

    df_initial = df[df.initial_visit == 1]

    df_followup = df[df.followup_visit == 1]
    df_followup = df_followup[right_cols]

    df_ipt = df[df.preipt_visit == 1]
    df_ipt = df_ipt[right_cols]

    df_final = df_initial.join(df_followup.set_index('case_id'), on='case_id', rsuffix='_ifu')
    df_final = df_final.join(df_ipt.set_index('case_id'), on='case_id', rsuffix='_ipt')
    df_final['followup_visit'] = df_final['followup_visit_ifu']
    df_final['preipt_visit'] = df_final['preipt_visit_ipt']
    df_final = df_final.drop(columns=['followup_visit_ifu', 'followup_visit_ipt', 'preipt_visit_ifu', 'preipt_visit_ipt'])

    #wtr = pandas.ExcelWriter(outfile)
    df_final.to_csv(outfile, index=False)

def main():
    parser = argparse.ArgumentParser(description='Process form data')
    parser.add_argument('--infile', help='Name of CSV file to read')
    parser.add_argument('--outfile', help='Name of CSV file to write')

    args = parser.parse_args()

    flatten(args.infile, args.outfile)

main()
