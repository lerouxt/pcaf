#!/usr/bin/env python3

import requests
import json
import argparse
import logging
import dpath
import csv

logging.basicConfig(level=logging.INFO)

class Forms():

    APP='blakeleylowry-test'
    APP_ID='c5d7bd78d98bc35d5f3af035ed09e929'
    API_PAGE_LIMIT=1000
    FIELDS = {
        'Followupcase' : 
            [ 'case/create/case_type', '@name',
              'ID', 'Date', 'Employment', 'Parish', 'Age', 'Tribe', 'Religion', 'Marital-status', 'Children-No',
              'Education-level', 'Sub-county', 'District', 'Village', 'Live-with', 'Household-Head',
              'PHQ2/total_PHQ2',
              'phq9/PHQ-9/PHQ9_TOTAL',
              'Functioning/FUNCTIONING/Fx_total'
            ],

        'KITGUM_SCREENING_TOOLS' : 
            [ 'case/create/case_type', '@name',
              'KID', 'Date', 'employment', 'parish', 'age', 'Ethnicity', 'religion', 'marital_status', 'children_no',
              'education_level', 'sub-county', 'District', 'village', 'live_with', 'hh_head',
              'PHQ2/PHQ_TOTAL',
              'PHQ9/PHQ9/PHQ9_GRAND_TOTAL', 
              'FUNCTIONING/Functioning/Fx_total'
            ],
        }
    HEADER = FIELDS['Followupcase'] # for now

    #APP='pcaf-poc'

    def __init__(self, apikeyfile, infile=None, outfile=None):
        self.apikey = self._get_api_key(apikeyfile)
        self.headers = { 'Authorization': self.apikey }
        self.infile=infile
        self.outfile=outfile
        self._build_lookups()

    def get_app(self):
        r = requests.get('https://www.commcarehq.org/a/{}/api/v0.5/application/{}'.format(self.APP, self.APP_ID), headers=self.headers )
        r.raise_for_status()
        return r

    def _build_lookups(self):
        app = self.get_app().json()
        self.values = {}
        for module in app['modules']:
            for forms in module['forms']:
                for question in forms['questions']:
                    value = question['value'][6:]
                    self.values[value] = {}
                    if 'options' in question:
                        for option in question['options']:
                            self.values[value][option['value']] = option['label']
        #print(self.values)

    def _get_api_key(self, filename):
        with open(filename) as f:
            return f.readline().strip()

    def get_form(self, form_id):
        r = requests.get('https://www.commcarehq.org/a/{}/api/v0.5/form/{}'.format(self.APP, form_id), headers=self.headers )
        r.raise_for_status()
        print(r.text)

    def dump(self):
        r = requests.get('https://www.commcarehq.org/a/{}/api/v0.4/form/?limit=1000'.format(self.APP), headers=self.headers )
        r.raise_for_status()
        print(r.text)

    def execute(self):

        logging.info('Writing to {}'.format(self.outfile))
        with open(self.outfile, 'w') as csvfile:
            wtr = csv.writer(csvfile)
            wtr.writerow(self.HEADER)

            if self.infile:
                logging.info('Opening {}'.format(self.infile))
                with open(self.infile) as _file:
                    jdata = json.load(_file)
                    
                    wtr.writerows(self.extract_data(jdata["objects"]))
            else:
                next_page = "?offset=0&limit={}".format(self.API_PAGE_LIMIT)

                while next_page:
                    url = 'https://www.commcarehq.org/a/{}/api/v0.4/form/{}'.format(self.APP, next_page)
                    logging.info('Fetching {}'.format(url))
                    r = requests.get(url, headers=self.headers)
                    r.raise_for_status()
                    jdata = r.json()
                    wtr.writerows(self.extract_data(jdata["objects"]))
                    next_page = jdata["meta"]["next"]
        
            #pdf = pandas.DataFrame(data=all_data, columns=self.FIELDS['Followupcase'])
            #pdf.to_pickle(self.outfile)


    def extract_data(self, objects):

        def get_path(case, key, default=None):
            try:
                value = dpath.util.get(case, key)
                if key in self.values:
                    if value in self.values[key]:
                        return self.values[key][value]
                return value
            except KeyError:
                return ""

        rows = []
        for case in objects:
            try:
                c = case['form']
                fields = self.FIELDS.get(c['case']['create']['case_type'])
                if fields:
                    rows.append([get_path(c, x) for x in fields])
            except KeyError:
                pass

        return rows
        
def main():
    parser = argparse.ArgumentParser(description='Extract form data from commcare')
    parser.add_argument('--dump', action='store_true', help='Dumps first few forms as json')
    parser.add_argument('--api-key-file', help='Sets the file containing the commcare API key')
    parser.add_argument('--get-form', help='Gets form from a form id')
    parser.add_argument('--get-app', action='store_true', help='Gets app')
    parser.add_argument('--infile', help='Optionally specifies filename of JSON instead of calling API')
    parser.add_argument('--outfile', default='out.csv', help='Specify where the output pickle file goes')
    args = parser.parse_args()

    forms = Forms(apikeyfile=args.api_key_file, infile=args.infile, outfile=args.outfile)
    if args.dump:
        forms.dump()
    elif args.get_app:
        print(forms.get_app().text)
    elif args.get_form:
        forms.get_form(args.get_form)
    else:
        forms.execute()
        pass

main()
