"""Blythe Kelly, Matt Colbert, Ujan RoyBandyopadhyay
December 2022

Run this script to update the CSV and JSON files in the data/ directory
using the files in the datasets/ directory.
"""

import csv
import json
import os

import pandas as pd

from tools import average, filter_by, year_from_filename


MEDIAN_DATASET = 'datasets/FY2001-2018-50-percentile/'
CRAIGSLIST_DATASET = 'datasets/clean_2000_2018.csv'
HOMELESSNESS_DATASET = 'datasets/Group Data Homeless.csv'

BAY_ALL_PATH = 'data/all_bay_data.json'
BEDS_PATH = 'data/bay_data.csv'
STATES_PATH = 'data/national_data.csv'
SQFT_PATH = 'data/sqft_data.json'
HOMELESSNESS_PATH = 'data/homelessness_data.csv'


def save_beds_data(load_path: str = CRAIGSLIST_DATASET,
                   save_path: str = BEDS_PATH):
    """Save median rent data for the Bay Area to a CSV file.

    The median rent data is obtained from a CSV file at the specified
    load path. It is then processed to calculate the median rent for
    listings in the Bay Area with a particular number of bedrooms for
    each year. The processed data is saved to a CSV file at the
    specified save path.

    Parameters:
        - load_path (str)
            path to CSV file containing raw median rent data
        - save_path (str)
            path where CSV file should be saved
    """
    # Load only the columns we need from the input CSV file.
    columns_to_load = ['year', 'price', 'beds']
    data = pd.read_csv(load_path, usecols=columns_to_load, low_memory=False)

    # Convert the 'beds' column to numeric values, and remove rows with
    # invalid values.
    data['beds'] = pd.to_numeric(data['beds'], errors='coerce')
    data = data.dropna(subset=['beds'])
    data['beds'] = data['beds'].astype(int)

    def median_rent(year: int, rooms: int) -> float:
        """Return the median rent for listings in the Bay Area with a
        particular number of bedrooms for a given year.
        """
        prices = data.query('year == @year & beds == @rooms')['price']
        return prices.median()

    # Create a list of years found in the data.
    years = sorted(data.year.unique())

    # Save the data as a CSV file.
    bay_pricing = [[median_rent(year, rooms) for year in years]
                   for rooms in range(5)]
    bay_df = pd.DataFrame(bay_pricing, columns=years)
    bay_df.to_csv(save_path)


def save_homelessness_data(load_path: str = HOMELESSNESS_DATASET,
                           save_path: str = HOMELESSNESS_PATH):
    """Save homelessness data from a CSV file to another CSV file.

    The homelessness data is read from the file at the specified load
    path and is then written to the file at the specified save path.

    Arguments:
        - load_path
            path to CSV file containing homelessness data
        - save_path
            path where CSV file should be saved
    """
    with open(load_path, mode='r') as load_file:
        data = csv.reader(load_file)

        # Copy data from load_file to save_file.
        with open(save_path, mode='w') as save_file:
            writer = csv.writer(save_file)
            for row in data:
                writer.writerow(row)


def save_national_data(folder: str = MEDIAN_DATASET,
                       save_path: str = STATES_PATH):
    """Save the national median rent data to a CSV file.

    The median rent data is obtained from Excel files in the specified
    folder and is then processed to calculate the average rent for each
    state and year. The processed data is saved to a CSV file at the
    specified save path.

    Arguments:
        - folder
            path to folder containing Excel files
        - save_path
            path where CSV file should be saved
    """
    # Create a dictionary of Excel data from the given folder using the
    # years from the filenames as keys.
    files = os.listdir(folder)
    data = {year_from_filename(file): pd.read_excel(folder + file)
            for file in files}

    # Define a function to determine whether a column should be kept.
    def keep(column: str) -> bool:
        return (column == 'state_alpha'
                or column.casefold().startswith('rent50'))

    # Drop extraneous columns from the data.
    for df in data.values():
        columns_to_drop = [col for col in df.columns if not keep(col)]
        df.drop(columns_to_drop, axis=1, inplace=True)
        df.dropna(inplace=True)

    # Store all state and year values found in the data.
    years = sorted(data.keys())
    states = data[years[0]].state_alpha.unique()

    def state_average(state: str, year: int, rooms: int) -> float:
        """Return the average rent (in a given state and year) for a
        property with a specified number of rooms.

        Arguments:
            - state
                state for which to calculate average price (if 'US',
                average will be calculated across all states)
            - year
            - rooms

        Returns:
            - float representing average price of property type
        """
        # Filter data by year and--unless national data is requested--
        # state.
        state_data = (data[year].dropna() if state == 'US' else
                      data[year].query('state_alpha == @state'))

        # Some of the datasets use slightly different column names.
        # Iterate through the three column name formats until the
        # correct one for the current year is found.
        column_names = (f'Rent50_{rooms}',
                        f'rent50_{rooms}',
                        f'Rent50_{rooms}Bed')
        for column in column_names:
            if column in state_data.columns:
                prices = [*state_data[column]]
                return average(prices)

    # Populate a list with average price data by state in a format that
    # can be converted to a pandas DataFrame.
    price_data = []
    for state in [*states, 'US']:
        state_data = [state]
        for year in years:
            year_data = [state_average(state, year, rooms)
                         for rooms in range(5)]
            state_data.append(year_data)
        price_data.append(state_data)

    df = pd.DataFrame(price_data, columns=['state_alpha', *years])
    df.to_csv(save_path)


def save_craigslist_data(load_path: str = CRAIGSLIST_DATASET,
                         save_avg_path: str = SQFT_PATH,
                         save_all_path: str = BAY_ALL_PATH):
    """Save average price per square foot data to a JSON file.

    The price and square foot data is obtained from a CSV file at the
    specified load path. It is then processed to calculate the average
    price per square foot for listings in each county in the Bay Area
    by year. The processed data and a list of all usable listings are
    saved to JSON files at the specified save paths.

    Parameters:
        - load_path
            path to CSV file containing raw rent data
        - save_avg_path
            path where JSON file containing average price per square
            foot data should be saved
        - save_all_path
            path where JSON file containing all listings should be
            saved
    """
    with open(load_path, mode='r') as file:
        raw_data = [*csv.DictReader(file)]

    # Create list of dictionaries containing relevant data for each
    # listing. Skip listings with invalid data.
    data = [{'year': int(listing['date'][:4]),
             'date': listing['date'],
             'price': int(listing['price']),
             'county': (listing['county'] if listing['county'] != 'NA'
                        else 'unknown / other'),
             'sqft': int(listing['sqft'])}
            for listing in raw_data
            if listing['sqft'].isnumeric()]

    # Store all state and year values found in the data.
    years = sorted({int(listing['year']) for listing in data})
    counties = {listing['county'] for listing in data}

    # Generate average prices per square foot by county and year.
    averages = [{'year': year,
                 'sqft_price': average(
                     [listing['price'] / listing['sqft']
                      for listing in filter_by(year, county, data)]
                 ),
                 'county': county}
                for year in years
                for county in counties]

    # Export and save data.
    with open(save_avg_path, mode='w') as file:
        json.dump(averages, file)

    with open(save_all_path, mode='w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    save_beds_data()
    save_homelessness_data()
    save_national_data()
    save_craigslist_data()