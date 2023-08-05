#!/usr/bin/env python3
"""\
usage: modaat.py
"""

__version__ = "0.2"

from sys import exit
import pandas as pd
from erddapy import ERDDAP
from .function import search_string, list_all_datasets, select_dataset, vars_in_dataset, attributes_in_dataset, \
    axis_in_dataset, get_sample_dataset, get_dataset


def main():
    loopctrl = True

    # define which server
    # TODO: implement in .env
    erddap_server_url = 'https://sig-gis.cen.ulaval.ca:8443/erddap'
    erddap_server_protocol = 'tabledap'
    erddap_server_response = 'csv'

    e = ERDDAP(server=erddap_server_url, protocol=erddap_server_protocol, response=erddap_server_response)

    df = pd.read_csv(e.get_search_url(response='csv', search_for='all'))

    dataset = None

    print(
        f'Welcome to {e.server} \n'
        f'We have {len(set(df["tabledap"].dropna()))} '
        f'tabledap, {len(set(df["griddap"].dropna()))} '
        f'griddap, and {len(set(df["wms"].dropna()))} wms endpoints.'
    )

    while loopctrl:
        print('Main menu:')
        print('1. List all available datasets')
        print('2. Search a string in the ERDDAP')
        print('3. Select a dataset to explore')
        print('4. Print all variables in dataset')
        print('5. Print all attributes in dataset')
        print('6. Print dataset axis labels')
        print('7. Print sample dataset')
        print('8. Get the whole dataset')
        print('0. Quit')

        if dataset is None:
            pass
        else:
            print('Selected dataset to explore:', dataset)

        menuitem = input("Enter your choice: ")

        match menuitem:
            case '1':
                list_all_datasets(e)
            case '2':
                search_string(e)
            case '3':
                dataset = select_dataset(e)
                print(dataset)
            case '4':
                if dataset is None or len(dataset) == 0:
                    print('No datasets selected. Please select a dataset (option 3).')
                    pass
                else:
                    vars_in_dataset(e, dataset)
            case '5':
                if dataset is None or len(dataset) == 0:
                    print('No datasets selected. Please select a dataset (option 3).')
                    pass
                else:
                    attributes_in_dataset(e, dataset)
            case '6':
                if dataset is None or len(dataset) == 0:
                    print('No datasets selected. Please select a dataset (option 3).')
                    pass
                else:
                    axis_in_dataset(e, dataset)
            case '7':
                if dataset is None or len(dataset) == 0:
                    print('No datasets selected. Please select a dataset (option 3).')
                    pass
                else:
                    get_sample_dataset(e, dataset)
            case '8':
                if dataset is None or len(dataset) == 0:
                    print('No datasets selected. Please select a dataset (option 3).')
                    pass
                else:
                    get_dataset(e, dataset)
            case '0':
                print('Exiting.')
                exit()
            case _:
                loopctrl = True


# Calling the application directly
if __name__ == "__main__":
    main()
