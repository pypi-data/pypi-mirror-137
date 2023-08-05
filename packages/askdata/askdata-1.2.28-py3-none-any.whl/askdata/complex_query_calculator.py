import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
import yaml


root_dir = os.path.abspath(os.path.dirname(__file__))
yaml_path = os.path.join(root_dir, '../askdata/askdata_config/base_url.yaml')
with open(yaml_path, 'r') as file:
    url_list = yaml.load(file, Loader=yaml.FullLoader)


def complex_field_calculator(instruction, dialect):

    if instruction is not "" and dialect is not "":

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "instruction": instruction,
            "dialect": dialect
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = url_list['BASE_URL_CFC_DEV'] + "/complexfieldcalculator"

        r = s.post(url=url, headers=headers, json=data)
        r.raise_for_status()

        try:
            response = r.json()['calculated_field']
            return response
        except Exception as e:
            logging.error(str(e))
            print(e)
            return None
    else:
        print("An input is empty!")
        return None


def complex_filter_calculator(instruction, dialect):

    if instruction is not "" and dialect is not "":

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "instruction": instruction,
            "dialect": dialect
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = url_list['BASE_URL_CFC_DEV'] + "/complexfiltercalculator"

        r = s.post(url=url, headers=headers, json=data)
        r.raise_for_status()

        try:
            response = r.json()['calculated_filter']
            return response
        except Exception as e:
            logging.error(str(e))
            print(e)
            return None
    else:
        print("An input is empty!")
        return None


def smartjoin(tables):

    if bool(tables):

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "tables": tables
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = url_list['BASE_URL_CFC_DEV'] + "/smartjoin"

        r = s.post(url=url, headers=headers, json=data)
        r.raise_for_status()

        try:
            response = r.json()['join_list']
            return response
        except Exception as e:
            logging.error(str(e))
            print(e)
            return None
    else:
        print("The input is empty!")
        return None
