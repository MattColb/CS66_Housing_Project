import json

import pandas as pd

from tools import formatted_date


def load_beds_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path).drop('Unnamed: 0', axis=1).transpose()

def load_listings_data(path: str) -> 'list[dict]':
    with open(path, mode='r') as file:
        data = json.load(file)

    # Replace date strings with datetime objects.
    for listing in data:
        listing['date'] = formatted_date(listing['date'])

    return data

def load_homelessness_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_sqft_data(path: str) -> 'list[dict]':
    with open(path, mode='r') as file:
        return json.load(file)

def load_states_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path).drop('Unnamed: 0', axis=1)