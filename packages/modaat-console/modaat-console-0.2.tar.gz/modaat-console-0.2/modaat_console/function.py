import urllib.error
import pandas as pd


def to_df(url_string):
    return pd.read_csv(url_string)


def search_string(erddap_conn):
    try:
        fields = ['Title', 'Institution', 'Dataset ID']
        search_for = input('What are you searching for? ')
        url = erddap_conn.get_search_url(search_for=search_for, response='csv')
        datasets = pd.read_csv(url, usecols=fields)
    except urllib.error.HTTPError:
        print('Expression not found.')
    else:
        print('Something was found in the following dataset(s):')
        print(datasets)


def list_all_datasets(erddap_conn):
    try:
        fields = ['Title', 'Institution', 'Dataset ID']
        search_str = 'all'
        url = erddap_conn.get_search_url(search_for=search_str, response='csv')
        datasets = pd.read_csv(url, usecols=fields)
    except urllib.error.HTTPError:
        print('Error.')
    else:
        print('Here are the datasets available on this server:')
        print(datasets)


# TODO: Validate the entry. Dataset ID not found should return a message
def select_dataset(erddap_conn):
    try:
        fields = ['Title', 'Dataset ID']
        search_dataset = input("Type the ID of a dataset you would like to explore. A valid example is "
                               "'downloads_d035_742e_ed6e'.  Type the ID: ")
        url = erddap_conn.get_search_url(search_for=search_dataset, response='csv')
        dataset = pd.read_csv(url, usecols=fields)
    except urllib.error.HTTPError:
        print('Error.')
    else:
        print('This dataset was selected:\n', dataset)
        return search_dataset


def vars_in_dataset(erddap_conn, dataset):
    try:
        print('Checking for variables in dataset', dataset)
        erddap_conn.dataset_id = dataset
        df = erddap_conn.to_pandas()
        print('Variables in dataset', dataset + ':')
        for index_col, col in enumerate(df.columns, start=1):
            print(index_col, col)
    except urllib.error.HTTPError:
        print('Error.')


def attributes_in_dataset(erddap_conn, dataset):
    try:
        url = erddap_conn.get_info_url(dataset, response="csv")
        df = pd.read_csv(url)
        print(df.values)
    except urllib.error.HTTPError:
        print('Error.')


def axis_in_dataset(erddap_conn, dataset):
    try:
        axis = erddap_conn.get_var_by_attr(dataset, axis=lambda v: v in ["X", "Y", "Z", "T"])
        print(axis)
    except urllib.error.HTTPError:
        print('Error.')


def get_sample_dataset(erddap_conn, dataset):
    try:
        # constraints : subsampling just first week of August 2018
        erddap_conn.constraints = {
            "time>=": "2018-08-01T00:00:00Z",
            "time<=": "2018-08-07T23:59:59Z",
        }

        erddap_conn.variables = {
            "time",
            "average_air_temperature",
        }

        erddap_conn.dataset_id = dataset
        df = erddap_conn.to_pandas()
        print(df)
        print('Direct download link = [' + erddap_conn.get_download_url() + ']')
        # After the task is complete, clear the constraints
        erddap_conn.constraints = None
    except urllib.error.HTTPError:
        print('Error.')


def get_dataset(erddap_conn, dataset):
    try:

        erddap_conn.variables = {
            "time",
            "average_air_temperature",
        }

        erddap_conn.dataset_id = dataset
        print('Direct download link = [' + erddap_conn.get_download_url() + ']')
    except urllib.error.HTTPError:
        print('Error.')
