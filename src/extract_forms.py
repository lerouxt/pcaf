#!/usr/bin/env python3

import requests
import json
import argparse
import logging
import dpath
import csv
import configparser

from collections import OrderedDict
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class Forms():
    """
    For the PHQ-2 scores, if the patient scores a "1" or "2" she is then referred 
    to the community health worker (CHW) for PHQ-9 screening; the cut-off for 
    depression is an "8" or above in Soroti and a "10" or above in Kitgum. 
    (Scores are different due to the prevalence and severity of depression in these 
    districts). For severe depression, the cut-off score is a "19" or above. 
    For suicidal, if the patient scores a 1,2,3.
    """

    FIELDS = {
        'Followupcase' : 
            [ 'case/create/case_type', '@name',
              'ID', 'Date', 'Employment', 'Parish', 'Age', 'Tribe', 'Religion', 'Marital-status', 'Children-No',
              'Education-level', 'Sub-county', 'District', 'Village', 'Live-with', 'Household-Head',
              'PHQ2/total_PHQ2',
              'phq9/PHQ-9/PHQ9-9!', 'phq9/PHQ-9/PHQ9_TOTAL',
              'PSYCHOEDUCATION',
              'Functioning/FUNCTIONING/Fx_total'
            ],

        'KITGUM_SCREENING_TOOLS' : 
            [ 'case/create/case_type', '@name',
              'KID', 'Date', 'employment', 'parish', 'age', 'Ethnicity', 'religion', 'marital_status', 'children_no',
              'education_level', 'sub-county', 'District', 'village', 'live_with', 'hh_head',
              'PHQ2/PHQ_TOTAL',
              'PHQ9/PHQ9/PHQ9_9!', 'PHQ9/PHQ9/PHQ9_GRAND_TOTAL', 
              'PSY_GIVEN_TO_POATIENT_',
              'FUNCTIONING/Functioning/Fx_total'
            ],
        }

    HEADER = [ 'case_type', 'form_name', 'id', 'date_created', 'employment', 'parish', 'age', 'tribe', 'religion',
               'marital_status', 'num_children', 'education_level', 'sub_county', 'district', 'village', 'live_with',
               'household_head', 'phq2_total', 'phq9_9', 'phq9_total', 'psychoeducation_flag', 'functioning_total',
                # following are computed and should match up with COMPUTED_FLAGS
               'date_download', 'region', 'depressed_flag', 'severely_depressed_flag', 'suicidal_flag'
             ]

    COMPUTED_DEFAULTS = [ datetime.now().isoformat(), 'Unknown', 0, 0, 0 ]

    def __init__(self, config_file, infile=None, outfile=None):
        config = configparser.ConfigParser()
        config.read(config_file)

        self.APIKEY = config.get('commcare', 'APIKEY')
        self.APP = config.get('commcare', 'APP')
        self.APP_ID = config.get('commcare', 'APP_ID')
        self.API_PAGE_LIMIT = config.getint('commcare', 'API_PAGE_LIMIT')

        self.headers = { 'Authorization': self.APIKEY }
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
            value = ""
            try:
                if not key.endswith('!'):
                    value = dpath.util.get(case, key)
                    if key in self.values:
                        if value in self.values[key]:
                            value = self.values[key][value]
                else:
                    value = dpath.util.get(case, key[:-1])

            except KeyError as e:
                pass
            return value

        rows = []
        for case in objects:
            try:
                c = case['form']
                fields = self.FIELDS.get(c['case']['create']['case_type'])
                if fields and c['@name'].startswith('Initial Screener'):
                    row = [get_path(c, x) for x in fields]
                    row = self.computed_columns(row, case)
                    rows.append(row)
            except KeyError as e:
                pass

        return rows

    def computed_columns(self, row, case):
        row.extend(self.COMPUTED_DEFAULTS)
        d = OrderedDict(zip(self.HEADER, row))

        region = d.get('case_type').strip()
        depressed_flag = 0
        severely_depressed_flag = 0
        phq9 = d.get('phq9_total', '')
        phq9 = int(phq9) if len(phq9) > 0 else 0

        if phq9 >= 19:
            severely_depressed_flag = 1

        phq9_9 = d.get('phq9_9', '')
        phq9_9 = int(phq9_9) if len(phq9_9) > 0 else 0
        suicidal_flag = 1 if phq9_9 > 0 else 0 

        if region == 'Followupcase':
            region = 'Soroti'
            if phq9 >= 8:
                depressed_flag = 1
        elif region == 'KITGUM_SCREENING_TOOLS':
            region = 'Kitgum'
            if phq9 >= 10:
                depressed_flag = 1

        d['region'] = region
        d['depressed_flag'] = depressed_flag
        d['severely_depressed_flag'] = severely_depressed_flag
        d['suicidal_flag'] = suicidal_flag

        if len(d['id']) == 0:
            print('Missing id: {}'.format(json.dumps(case)))

        return d.values()
        
def main():
    parser = argparse.ArgumentParser(description='Extract form data from commcare')
    parser.add_argument('--dump', action='store_true', help='Dumps first few forms as json')
    parser.add_argument('--config-file', default='pcaf.cfg', help='Sets the config file')
    parser.add_argument('--get-form', help='Gets form from a form id')
    parser.add_argument('--get-app', action='store_true', help='Gets app')
    parser.add_argument('--infile', help='Optionally specifies filename of JSON instead of calling API')
    parser.add_argument('--outfile', default='out.csv', help='Specify where the output pickle file goes')
    args = parser.parse_args()

    forms = Forms(config_file=args.config_file, infile=args.infile, outfile=args.outfile)
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
