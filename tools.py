import datetime
from typing import Collection, Optional

import pandas as pd


def average(prices: Collection[float]) -> Optional[float]:
    """Return the average of an iterable of numbers.

    When the iterable is empty, return None. Averages are rounded to
    two decimal digits.

    Arguments:
        - prices
            an iterable of numeric values

    Returns:
        float representing the average price
    """
    if prices:
        return round(sum(prices) / len(prices), ndigits=2)
    return None


def filter_by(year: int, county: str, data: 'list[dict]') -> filter:
    """Return the listings for a specific county and year.

    Arguments:
        - year
        - county
        - data
            list of dictionaries representing listings, each of which
            must contain 'year' and 'county' keys

    Returns:
        filter object containing listings for county and year
    """
    return filter(lambda x: x['year'] == year and x['county'] == county, data)


def find_correlation(df: pd.DataFrame, col1: str, col2: str) -> float:
    """Return the correlation between two pandas columns in a DataFrame.

    Arguments:
        - df
            pandas DataFrame
        - col1
            name of first column
        - col2
            name of second column

    Returns:
        - float representing the correlation between the two columns
    """
    return df[col1].corr(df[col2])


def formatted_date(date: str, /) -> datetime.date:
    """Return a datetime.date from a yyyymmdd string.

    Arguments:
        - date
            yyyymmdd string

    Returns:
        datetime.date representing the date passed to the function
    """
    year, month, day = date[:4], date[4:6], date[6:]
    return datetime.date(int(year), int(month), int(day))


def evaluate_list_literal(x: str, /) -> 'list[str]':
    """Take a string as input and return a list of strings.

    The input string is expected to be in the format of a list literal
    (e.g. '[5, 7, 8]'), and the output list will contain the items from
    the input in the form of a list (e.g. [5, 7, 8]).

    Arguments:
        - x
            input string containing a list literal

    Returns:
        - list of strings
    """
    return x.split('[')[1].split(']')[0].split(',')


def year_from_filename(filename: str, /) -> int:
    """Return the year from the name of a file in the national dataset.

    Arguments:
        - filename

    Returns:
    An integer representing the year in the filename.
    """
    return int(filename[2:6])