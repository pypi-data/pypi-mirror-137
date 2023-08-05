Lochness: Sync data from all over the cloud to a local directory
================================================================
Lochness is a data management tool designed to periodically poll and 
download data from various data archives into a local directory. This 
is often referred to as building a "data lake" (hence the name).

Out of the box there is support for pulling data down from Beiwe, XNAT, 
REDCap, Dropbox, external hard drives, and more. Extending Lochness to 
support new services is also a fairly simple process.

## Table of contents
1. [Installation](#installation)
2. [Quick setup from a template](#setup-from-a-template)
3. [Documentation](http://docs.neuroinfo.org/lochness/en/latest/)


## Installation

Just use `pip`

```
pip install lochness
```


For most recent DPACC-lochness

```
pip install git+https://github.com/PREDICT-DPACC/lochness
```


For debugging

```
cd ~
git clone https://github.com/PREDICT-DPACC/lochness
pip install -r ~/lochness/requirements.txt

export PATH=${PATH}:~/lochness/scripts  # add to ~/.bashrc
export PYTHONPATH=${PYTHONPATH}:~/lochness  # add to ~/.bashrc
```


## Running test

- Copy the token template, and add the information for each module.

```
cd lochness/tests
cp token_template_for_test_template.csv token_template_for_test.csv
```

- Run test
```
bash run_test.sh 
```


## Setup from a template

### Creating the template
Setting up lochness from scratch could be slightly confusing in the beginning.
Try using the `lochness_create_template.py` to create a starting point.

Create an example template to easily structure the lochness system

```sh
# ProNET
lochness_create_template.py \
    --outdir /data/lochness_root \
    --studies PronetLA PronetSL PronetWU \
    --sources redcap xnat box mindlamp \
    --email kevincho@bwh.harvard.edu \
    --poll_interval 43200 \
    --ssh_host erisone.partners.org \
    --ssh_user kc244 \
    --lochness_sync_send \
    --s3

# PRESCIENT
lochness_create_template.py \
    --outdir /data/lochness_root \
    --studies PrescientAD PrescientME PrescientPE \
    --sources RPMS mediaflux mindlamp \
    --email kevincho@bwh.harvard.edu \
    --poll_interval 43200 \
    --ssh_host erisone.partners.org \
    --ssh_user kc244 \
    --lochness_sync_send \
    --s3

# For more options: lochness_create_template.py -h
```


### Making edits to the template

Running one of the commands above will create the structure below

```sh
/data/lochness_root/
├── 1_encrypt_command.sh
├── 2_sync_command.sh
├── PHOENIX
│   ├── GENERAL
│   │   ├── PronetLA
│   │   │   └── PronetLA_metadata.csv
│   │   ├── PronetSL
│   │   │   └── PronetSL_metadata.csv
│   │   └── PronetWU
│   │       └── PronetWU_metadata.csv
│   └── PROTECTED
│       ├── PronetLA
│       ├── PronetSL
│       └── PronetWU
├── config.yml
├── lochness.json
└── pii_convert.csv
```


1. Change information in `config.yml` and `lochness.json` as needed.


2. Either manually update the `PHOENIX/GENERAL/*/*_metadata.csv` or
   amend the field names in REDCap / RPMS sources correctly for lochness to
   automatically update the metadata files.

   Currently, lochness initializes the metadata using the following field names 
   in REDCap and RPMS.

- `chric_subject_id`: the record ID field name
    - this field name must be in the REDCap or RPMS repository for the metadata
      to be updated by lochness.
- `chric_consent_date`: the field name of the consent date
    - this field name must be in the REDCap or RPMS repository for the metadata
      to be updated by lochness.
- `beiwe_id`: the field name of the BEIWE ID.
- `xnat_id`: the field name of the XNAT ID.
- `dropbox_id`: the field name of the Dropbox ID.
- `box_id`: the field name of the Box ID.
- `mediaflux_id`: the field name of the Mediaflux ID.
- `mindlamp_id`: the field name of the Mindlamp ID.
- `daris_id`: the field name of the DaRIS ID.
- `rpms_id`: the field name of the RPMS ID.


3. Encrypt the `lochness.json` by running

```sh
cd /data/lochness_root
bash 1_encrypt_command.sh
```

This encryption step creates a copy of encrypted keyrings to
`/data/lochness_root/.lochness.enc`. To protect the sensitive keyring
information in json, remove the `lochness.json` after running the encryption.


You can still extract keyring structure without sensitive information by running

```
lochness_check_config.py -ke /data/lochness_root/.lochness.enc
```


4. Set up REDCap Data Entry Trigger if using REDCap. Please see below 
   "REDCap Data Entry Trigger capture" section.


5. Edit Personally identifiable information mapping table. Please seee below
   "Personally identifiable information removal from REDCap and RPMS data"

> /data/lochness_root/pii_convert.csv


5. Run the `sync.py` or use the example command in `2_sync_command.sh`

> bash 2_sync_command.sh



### To use `lochness_to_lochness` transfer through `aws s3`

1. Set up s3 bucket
2. Install aws CLI
3. Configure CLI with your s3 bucket information

`$ aws configure`

4. Add your AWS information to `config.yml`

```
AWS_BUCKET_NAME: ampscz-dev
AWS_BUCKET_ROOT: TEST_PHOENIX_ROOT
```


### REDCap Data Entry Trigger capture

If your sources include REDCap and you would like to configure lochness to 
only pull new REDCap data, "Data Entry Trigger" needs to be set up in REDCap.

In REDCap,
- "Project Setup"
- "Enable optional modules and customizations"
- "Additional customizations"
- Check "Data Entry Trigger" and give address of the server including the port number e.g. http://pnl-t55-7.partners.org:9999


In order to use this functionality, the server where lochness is installed
should be able to receieve HTTP POST signal from REDCap server. Which means it
has to be either

- lochness server is inside the same firewall as REDCap server.
    Or
- lochness server has a open port that could listen to the REDCap POST signal.


After setting the "Data Entry Trigger" on REDCap settings, run below to update
the `/data/data_entry_trigger_db.csv` real-time

```
# please specify the same port defined in the REDCap settings
listen_to_redcap.py --database_csv /data/data_entry_trigger_db.csv \
                    --port 9999
```


It would be useful to run `listen_to_redcap.py` in background, maybe inside a
`gnu screen` so it runs continuously without interference.



### Personally identifiable information removal from REDCap and RPMS data

A path of csv file can be provided, which has information about how to process
each PII fields. 

For example

> /data/personally_identifiable_process_mappings.csv

```table
pii_label_string | process
-----------------|---------------
address          | remove
date             | change_date
phone_number     | random_number
patient_name     | random_string
subject_name     | replace_with_subject_id
```

Any value from the field, with names that match to `pii_label_string` rows,
the labelled **PII processing method** will be used to process the raw values
to remove or replace the PIIs.


## Documentation
You can find all the documentation you will ever need [here](https://lochness.readthedocs.io/en/latest/)
