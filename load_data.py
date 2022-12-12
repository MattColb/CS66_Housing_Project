import json

import pandas as pd


def load_bay_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path).drop('Unnamed: 0', axis=1).transpose()

def load_craigslist_data(path: str) -> 'list[dict]':
    with open(path, mode='r') as file:
        return json.load(file)

def load_homelessness_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_sqft_data(path: str) -> 'list[dict]':
    with open(path, mode='r') as file:
        return json.load(file)

def load_states_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path).drop('Unnamed: 0', axis=1)