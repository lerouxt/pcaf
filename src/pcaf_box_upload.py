#!/usr/bin/env python3

import logging
import argparse
import configparser
from box import Box

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description='Process form data')
    parser.add_argument('--config-file', default='pcaf.cfg', help='Name of config file')
    parser.add_argument('--infile', help='Name of file to upload')
    parser.add_argument('--boxname', help='Name of file as it will appear in box')

    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config_file)

    USER_ID = config.get('pcafboxupload', 'USER_ID')
    DIRECTORY = config.get('pcafboxupload', 'DIRECTORY')

    Box(config).upload_file(USER_ID, args.infile, args.boxname, DIRECTORY)

main()
