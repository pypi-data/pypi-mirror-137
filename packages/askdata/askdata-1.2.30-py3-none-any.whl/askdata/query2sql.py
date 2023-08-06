import json
import jsons
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import requests
import os
import yaml


root_dir = os.path.abspath(os.path.dirname(__file__))
yaml_path = os.path.join(root_dir, '../askdata/askdata_config/base_url.yaml')
with open(yaml_path, 'r') as file:
    url_list = yaml.load(file, Loader=yaml.FullLoader)


def query_to_sql(smartquery, db_driver):
    # Google Pod
    headers = {
        "Content-Type": "application/json"
    }

    s = requests.Session()
    s.keep_alive = False
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    url = url_list['BASE_URL_QUERY2SQL_DEV'] + "/query_to_sql"

    stringed_smartquery = jsons.dumps(smartquery, strip_nulls=True)
    smartquery = json.loads(stringed_smartquery)

    data = {
        "smartquery": smartquery,
        "db_driver": db_driver
    }

    r = s.post(url=url, headers=headers, json=data)
    r.raise_for_status()

    try:
        dict_response = r.json()
        translation = dict_response['translation']
        return translation
    except Exception as e:
        logging.error(str(e))


def query_to_olap(nl, schema=None, df=None, db_driver="olap"):

    if not (schema is None and df is None):

        # Google Pod
        headers = {
            "Content-Type": "application/json"
        }

        if df is not None:
            dict_df = df.to_dict()
        else:
            dict_df = {}

        if schema is None:
            schema = {}

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = url_list['BASE_URL_QUERY2SQL_DEV'] + "/query_to_olap"

        data = {
            "nl_query": nl,
            "table_schema": schema,
            "df": dict_df
        }

        r = s.post(url=url, headers=headers, json=data)
        r.raise_for_status()

        try:
            dict_response = r.json()
            nl_ner = dict_response['nl_ner']
            return nl_ner
        except Exception as e:
            logging.error(str(e))
    else:
        print("Schema is empty and DataFrame is empty.")
        return None


def prepare_ner(nl, schema=None, df=None, db_driver="olap"):

    if not (schema is None and df is None):

        # Google Pod
        headers = {
            "Content-Type": "application/json"
        }

        if df is not None:
            dict_df = df.to_dict()
        else:
            dict_df = {}

        if schema is None:
            schema = {}

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = url_list['BASE_URL_QUERY2SQL_DEV'] + "/prepare_ner"

        data = {
            "nl_query": nl,
            "table_schema": schema,
            "df": dict_df
        }

        r = s.post(url=url, headers=headers, json=data)
        r.raise_for_status()

        try:
            dict_response = r.json()
            nl_ner = dict_response['nl_ner']
            return nl_ner
        except Exception as e:
            logging.error(str(e))
    else:
        print("Schema is empty and DataFrame is empty.")
        return None


def query_to_smartquery(query):

    if query is not None:

        # Google Pod
        headers = {
            "Content-Type": "application/json"
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = url_list['BASE_URL_QUERY2SQL_DEV'] + "/query_to_smartquery"

        data = {
            "query": query
        }

        r = s.post(url=url, headers=headers, json=data)
        r.raise_for_status()

        try:
            dict_response = r.json()
            smartquery = dict_response['smartquery']
            return smartquery
        except Exception as e:
            logging.error(str(e))
    else:
        print("Schema is empty and DataFrame is empty.")
        return None


def smartquery_to_olap(smartquery):

    if smartquery is not None:

        # Google Pod
        headers = {
            "Content-Type": "application/json"
        }

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = url_list['BASE_URL_QUERY2SQL_DEV'] + "/smartquery_to_olap"

        data = {
            "smartquery": smartquery
        }

        r = s.post(url=url, headers=headers, json=data)
        r.raise_for_status()

        try:
            dict_response = r.json()
            nl_ner = dict_response['nl_ner']
            return nl_ner
        except Exception as e:
            logging.error(str(e))
    else:
        print("Schema is empty and DataFrame is empty.")
        return None
