#!/bin/sh
PYTHON=/home/ubuntu/src/pcaf/bin/python3

cd /home/ubuntu/src/pcaf/src

echo "Extracting data"
$PYTHON ./extract_forms.py --extract --outfile pcaf.csv
$PYTHON ./forms_to_xls.py --infile pcaf.csv --outfile pcaf.xls

# upload to PCAF Bot Home Dir
echo "Uploading to bot folder"
$PYTHON ./pcaf_box_upload.py --infile pcaf.xls --boxname pcaf.xls --file-id 252100845592
echo "Uploading to PCAF shared folder"
$PYTHON ./pcaf_box_upload.py --infile pcaf.xls --boxname pcaf.xls --file-id 252100680089

echo "Backup up to S3"
aws s3 cp pcaf.csv s3://pcaf-dataset/cases/csv/pcaf.csv
aws s3 cp pcaf.xls s3://pcaf-dataset/cases/xls/pcaf.xls
