#!/usr/bin/env python3

import requests
import json
import argparse
import logging
import dpath
import pandas

logging.basicConfig(level=logging.INFO)


class Forms():

    APP='blakeleylowry-test'
    APP_ID='c5d7bd78d98bc35d5f3af035ed09e929'
    #APP='pcaf-poc'

    def __init__(self, apikey=None, file=None):
        self.apikey = apikey
        self.HEADERS = { 'Authorization': apikey }
        self.file=file

    def get_app(self):
        r = requests.get('https://www.commcarehq.org/a/{}/api/v0.5/application/{}'.format(self.APP, self.APP_ID), headers=self.HEADERS )
        r.raise_for_status()
        return r.json()

    def build_lookups(self):
        app = self.get_app()
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
        r = requests.get('https://www.commcarehq.org/a/{}/api/v0.5/form/{}'.format(self.APP, form_id), headers=self.HEADERS )
        r.raise_for_status()
        print(r.text)

    def dump(self):
        r = requests.get('https://www.commcarehq.org/a/{}/api/v0.4/form/'.format(self.APP), headers=self.HEADERS )
        r.raise_for_status()
        print(r.text)

    def show_forms(self):
        fields = ('ID', 'Employment', 'Parish', 'Age', 'Tribe', 'Religion', 'Marital-status', 'Children-No',
                  'Education-level', 'Sub-county', 'District', 'Village', 'Live-with', 'Household-Head',
                  'PHQ2/PHQ2_1', 'PHQ2/PHQ2_2', 'PHQ2/total_PHQ2', 'PHQ2/Completed_by',
                  'phq9/PHQ-9/PHQ9-1', 'phq9/PHQ-9/PHQ9-2', 'phq9/PHQ-9/PHQ9-3', 
                  'phq9/PHQ-9/PHQ9-4', 'phq9/PHQ-9/PHQ9-5', 'phq9/PHQ-9/PHQ9-6', 'phq9/PHQ-9/PHQ9-7', 
                  'phq9/PHQ-9/PHQ9-8', 'phq9/PHQ-9/PHQ9-9'
                )
        jdata = None

        def get_path(case, key, default=None):
            try:
                value = dpath.util.get(case, key)
                if key in self.values:
                    if value in self.values[key]:
                        return self.values[key][value]
                return value
            except KeyError:
                return ""

        if self.file:
            logging.info('opening {}'.format(self.file))
            with open(self.file) as _file:
                jdata = json.load(_file)
        else:
            r = requests.get('https://www.commcarehq.org/a/{}/api/v0.4/form/'.format(self.APP), headers=self.HEADERS )
            r.raise_for_status()
            jdata = r.json()

        all_data = []
        for case in jdata["objects"]:
            try:
                c = case['form']
                if c['case']['create']['case_type'] == 'Followupcase':
                    row = list(get_path(c, x) for x in fields)
                    all_data.append(row)

            except KeyError:
                pass

        #print(all_data)
        pdf = pandas.DataFrame(data=all_data, columns=fields)
        print(pdf)

def main():
    parser = argparse.ArgumentParser(description='Process form data')
    parser.add_argument('--dump', action='store_true', help='Dumps first few forms as json')
    parser.add_argument('--apikey', help='Sets the commcare API key')
    parser.add_argument('--get-form', help='Gets form from a form id')
    parser.add_argument('--file', help='Optionally specifies filename of JSON instead of calling API')
    args = parser.parse_args()

    forms = Forms(apikey=args.apikey, file=args.file)
    if args.dump:
        forms.dump()
    elif args.get_form:
        forms.get_form(args.get_form)
    else:
        forms.build_lookups()
        forms.show_forms()

main()
