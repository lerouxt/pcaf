#!/usr/bin/env python3

import requests
import json
import argparse
import dpath
import csv
import configparser
import ijson

from datetime import datetime
from copy import copy

from field_mapping import HEADER
from field_mapping import FORM_MAPPING

class Forms():
    """
    For the PHQ-2 scores, if the patient scores a "1" or "2" she is then referred 
    to the community health worker (CHW) for PHQ-9 screening; the cut-off for 
    depression is an "8" or above in Soroti and a "10" or above in Kitgum. 
    (Scores are different due to the prevalence and severity of depression in these 
    districts). For severe depression, the cut-off score is a "19" or above. 
    For suicidal, if the patient scores a 1,2,3.
    """

    def __init__(self, config_file, infile=None, outfile=None, rejectfile=None, debug=False):
        config = configparser.ConfigParser()
        config.read(config_file)

        self.APIKEY = config.get('commcare', 'APIKEY')
        self.APP = config.get('commcare', 'APP')
        self.APP_ID = config.get('commcare', 'APP_ID')
        self.API_PAGE_LIMIT = config.getint('commcare', 'API_PAGE_LIMIT')

        self.headers = { 'Authorization': self.APIKEY }
        self.infile=infile
        self.outfile=outfile
        self.rejectfile=rejectfile
        self.debug=debug
        self.values=self.get_lookups()

    def get_app(self):
        r = requests.get('https://www.commcarehq.org/a/{}/api/v0.5/application/{}'.format(self.APP, self.APP_ID), headers=self.headers )
        r.raise_for_status()
        return r

    def get_lookups(self):
        app = self.get_app().json()
        values = {}
        for module in app['modules']:
            for forms in module['forms']:
                for question in forms['questions']:
                    value = question['value'][6:]
                    values[value] = {}
                    if 'options' in question:
                        for option in question['options']:
                            values[value][option['value']] = option['label']
        return values

    def dump_lookups(self):
        print(json.dumps(self.values, indent=4))

    def get_form(self, form_id):
        r = requests.get('https://www.commcarehq.org/a/{}/api/v0.5/form/{}'.format(self.APP, form_id), headers=self.headers )
        r.raise_for_status()
        print(r.text)

    def dump(self):
        r = requests.get('https://www.commcarehq.org/a/{}/api/v0.4/form/?offset=0&limit=100'.format(self.APP), headers=self.headers)
        r.raise_for_status()
        print(json.dumps(r.json(), indent=3))

    def extract_from_commcare(self):
        next_page = "?offset=0&limit={}".format(self.API_PAGE_LIMIT)

        while next_page:
            url = 'https://www.commcarehq.org/a/{}/api/v0.4/form/{}'.format(self.APP, next_page)
            print('Fetching {}'.format(url))
            r = requests.get(url, headers=self.headers)
            r.raise_for_status()
            jdata = r.json()
            for obj in jdata["objects"]:
                yield obj
            next_page = jdata["meta"]["next"]

    def extract_from_file(self):
        with open(self.infile) as _file:
            objects = ijson.items(_file, "objects.item")
            for obj in objects:
                yield obj

    def extract_from_iter(self, objects):
        record = 0
        with open(self.rejectfile, 'w') as _rejectfile:
            with open(self.outfile, 'w') as _outfile:
                wtr = csv.DictWriter(_outfile, fieldnames=[ row[0] for row in HEADER ])
                wtr.writeheader()
                for o in objects:
                    try:
                        record += 1
                        # THESE are required fields
                        form_name = o['form']['@name']
                        case_id = o['form']['case']['@case_id']
                        form_id = o['form']['@xmlns']
                        row = self.extract_data(case_id, form_id, o['form'])
                        if row:
                            wtr.writerow(row)
                    except KeyError as e:
                        _rejectfile.write("\nERROR processing record {}: {}\n".format(record, str(e)))
                        _rejectfile.write(json.dumps(o, indent=4))

    def extract_data(self, case_id, form_id, data):
        row = copy(FORM_MAPPING.get(form_id))
        if row:
            for field, loc in row.items():
                value = None
                do_lookup = False
                if loc.endswith('!'):
                    row[field] = loc[:-1]
                else:
                    if loc.endswith('?'):
                        do_lookup = True
                        loc = loc[:-1]

                    try:
                        value = dpath.util.get(data, loc)
                        if do_lookup and loc in self.values and value in self.values[loc]:
                            value = self.values[loc][value]
                    except KeyError as e:
                        if self.debug:
                            print("Missing field {} at {} on form {} for case {}".format(field, loc, form_id, case_id))
                    row[field] = value
            try:
                row = self.add_computed_columns(row)
            except Exception as e:
                print("Error during compute for form {} for case {}".format(form_id, case_id))
                print(row)
                raise
        return row

    def add_computed_columns(self, row):
        depressed_flag = 0
        severely_depressed_flag = 0
        phq9 = row.get('phq9_total', '')
        phq9 = '' if phq9 is None else phq9
        phq9 = int(phq9) if len(phq9) > 0 else 0

        if phq9 >= 19:
            severely_depressed_flag = 1

        phq9_9 = row.get('phq9_9', '')
        phq9_9 = '' if phq9_9 is None else phq9_9
        phq9_9 = int(phq9_9) if len(phq9_9) > 0 else 0
        suicidal_flag = 1 if phq9_9 > 0 else 0 

        if row['region'] == 'Soroti':
            if phq9 >= 8:
                depressed_flag = 1
        elif row['region'] == 'Kitgum':
            if phq9 >= 10:
                depressed_flag = 1

        row['depressed_flag'] = depressed_flag
        row['severely_depressed_flag'] = severely_depressed_flag
        row['suicidal_flag'] = suicidal_flag

        return row
        
def main():
    parser = argparse.ArgumentParser(description='Extract form data from commcare')
    parser.add_argument('--debug', action='store_true', help='Turns debug mode on')
    parser.add_argument('--dump', action='store_true', help='Dumps all forms as json')
    parser.add_argument('--dump-lookups', action='store_true', help='Dumps form lookup data')
    parser.add_argument('--config-file', default='pcaf.cfg', help='Sets the config file')
    parser.add_argument('--get-form', help='Gets form from a form id')
    parser.add_argument('--get-app', action='store_true', help='Gets app')
    parser.add_argument('--infile', help='Optionally specifies filename of JSON instead of calling API')
    parser.add_argument('--outfile', default='out.csv', help='Specify where the output pickle file goes')
    parser.add_argument('--rejectfile', default='rejects.out', help='Unparseable forms go into this file')
    parser.add_argument('--extract', action='store_true', help='Extracts csv data from json dump')
    args = parser.parse_args()

    forms = Forms(config_file=args.config_file, infile=args.infile, outfile=args.outfile, rejectfile=args.rejectfile, debug=args.debug)
    if args.dump:
        forms.dump()
    elif args.dump_lookups:
        forms.dump_lookups()
    elif args.get_app:
        print(forms.get_app().text)
    elif args.get_form:
        forms.get_form(args.get_form)
    elif args.extract:
        if args.infile:
            forms.extract_from_iter(forms.extract_from_file())
        else:
            forms.extract_from_iter(forms.extract_from_commcare())

main()
