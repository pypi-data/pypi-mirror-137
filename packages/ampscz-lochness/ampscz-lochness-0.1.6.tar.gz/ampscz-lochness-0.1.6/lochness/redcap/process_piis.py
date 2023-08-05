import lochness
import pandas as pd
from pathlib import Path
import json
import random
import string
from datetime import date
from typing import List
import re
import sys


class PiiTableError(Exception):
    pass


def read_pii_mapping_to_dict(pii_table_loc: str) -> pd.DataFrame:
    '''Read PII process table and return as dict

    Any field name containing the pii_label_string will be processed
    accordingly.

    Key arguments:
        pii_table_loc: path of the PII field string and process method csv

    Table example:
        pii_label_string | process
        -----------------|---------------
        address          | remove
        date             | change_date
        phone_number     | random_number
        patient_name     | random_string
        subject_name     | replace_with_subject_id
    '''

    if Path(pii_table_loc).is_file():
        df = pd.read_csv(pii_table_loc)

        # make sure the df is in the correct format
        # if df.columns != ['pii_label_string', 'process']:
        if not 'pii_label_string' in df.columns or not 'process' in df.columns:
            raise PiiTableError('pii_table is not in the right format')

        if len(df) < 1:
            raise PiiTableError('pii_table is not in the right format')

        pii_string_process_dict = df.set_index(
                'pii_label_string')['process'].to_dict()
    else:
        pii_string_process_dict = {}

    return pii_string_process_dict


def load_raw_return_proc_json(json_loc: str,
                              pii_str_proc_dict: dict,
                              subject_id: str) -> List[dict]:
    # load json in PROTECTED/survey/raw
    with open(json_loc, 'r') as f:
        raw_json = json.load(f)  # list of dicts

    processed_json = []
    for instrument in raw_json:
        processed_instrument = {}
        for field_name, field_value in instrument.items():
            for pii_label_string, process in pii_str_proc_dict.items():
                if re.search(pii_label_string, field_name):
                    try:
                        new_value = process_pii_string(field_value,
                                                       process,
                                                       subject_id)
                    except:
                        new_value = 'check_process_pii_string'
                    processed_instrument[field_name] = new_value
                    break
                else:
                    processed_instrument[field_name] = field_value
        processed_json.append(processed_instrument)

    processed_content = json.dumps(processed_json).encode()

    return processed_content


def get_shuffle_dict_for_type(string_type: string, input_str: str) -> dict:
    '''Return strings randomised using random mapping of given string_type

    Key Arguments:
        string_type: string types, eg) string.digits or string.ascii_lowercase
        input_str: str

    Returns
        input_str: randomised str
    '''
    system_random = random.SystemRandom()

    from_alphabet = ''.join(
            system_random.choice(string_type) for i in range(26))
    to_alphabet = ''.join(
            system_random.choice(string_type) for i in range(26))
    old_2_new_dict = dict(zip(from_alphabet,
                              to_alphabet))

    for old, new in old_2_new_dict.items():
        input_str = re.sub(old, new, input_str)

    return input_str


def process_pii_string(pii_string: str, process: str, subject_id: str) -> str:
    '''Process PII string

    Key Arguments:
        - value_of_field: Raw value of the field, str.
        - process: How to process the raw value, str.
            - 'remove': completely remove the field from the json file.
            - 'change_date': change to days from certain time point.
            - 'random_number': replaced to random numbers in the same length.
            - 'random_string': replaced to random strings in the same length.
            - 'replace_with_subject_id': replaced with subject_id

    Examples:
        process_pii_string('address': 'remove')
        process_pii_string('patient_name': 'random_string')
    '''


    if process == 'remove':
        return ''

    elif process == 'change_date':
        base_date = date(1900, 1, 1)

        # eg) 2016-10-03
        pii_string = pii_string.split(' ')[0]
        y = int(pii_string.split('-')[0])
        m = int(pii_string.split('-')[1])
        d = int(pii_string.split('-')[2])

        new_date = date(y, m, d)
        delta = new_date - base_date

        return str(delta.days)

    elif process == 'random_number':
        digits = string.digits
        return get_shuffle_dict_for_type(digits, pii_string)

    elif process == 'random_small_letters':
        letters = string.ascii_lowercase
        return get_shuffle_dict_for_type(letters, pii_string.lower())

    elif process == 'random_capital_letters':
        letters = string.ascii_uppercase
        return get_shuffle_dict_for_type(letters, pii_string.upper())

    elif process == 'random_string':
        system_random = random.SystemRandom()
        letters = string.ascii_lowercase
        new_string = ''.join(
            system_random.choice(letters) for i in range(len(pii_string)))
        return new_string

    elif process == 'replace_with_subject_id':
        return subject_id

    else:
        return pii_string


def load_raw_return_proc_csv(csv_loc: str,
                             pii_str_proc_dict: dict,
                             subject_id: str) -> List[dict]:
    '''CSV version of the load raw CSV and save processed CSV'''
    # load csv in PROTECTED/survey/raw
    raw_df_subject = pd.read_csv(csv_loc)

    for field_name in raw_df_subject.columns:
        field_value = raw_df_subject.loc[0][field_name]
        for pii_label_string, process in pii_str_proc_dict.items():
            if re.search(pii_label_string, field_name):
                try:
                    new_value = process_pii_string(field_value,
                                                   process,
                                                   subject_id)
                except:
                    new_value = 'check_process_pii_string'
                raw_df_subject.loc[0, field_name] = new_value
                break
            else:
                raw_df_subject.loc[0, field_name] = field_value

    return raw_df_subject


def process_and_copy_db(Lochness, subject, raw_input, proc_dst):
    '''Process PII and copy the json to GENERAL/survey/processed'''
    pii_table_loc = get_PII_table_loc(Lochness, subject.study)

    # don't run this if the pii_table in the config.yml is missing
    if pii_table_loc != False and pii_table_loc != '':
        # process PII here
        pii_str_proc_dict = read_pii_mapping_to_dict(pii_table_loc)

        if str(raw_input).endswith('json'):
            processed_content = load_raw_return_proc_json(
                    raw_input, pii_str_proc_dict, subject.id)

            # double check the pii string processing dict once more
            # if it's empty, don't copy it over to general
            if pii_str_proc_dict != {}:
                lochness.atomic_write(proc_dst, processed_content)

        elif str(raw_input).endswith('csv'):
            processed_df = load_raw_return_proc_csv(
                    raw_input, pii_str_proc_dict, subject.id)

            # double check the pii string processing dict once more
            # if it's empty, don't copy it over to general
            if pii_str_proc_dict != {}:
                processed_df.to_csv(proc_dst, index=False)



def get_PII_table_loc(Lochness, study):
    ''' get study specific deidentify flag with a safe default '''
    value = Lochness.get('pii_table', False)
    return value


