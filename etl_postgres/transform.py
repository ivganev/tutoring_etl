import pandas as pd

# Process the timestamps
def process_timestamp(row, time_stamp_attribute='start_timestamp') -> None:
    """Splits a timestamp represented by a datetime into its three parts"""
    date = pd.to_datetime(row[time_stamp_attribute])
    row['year'] = date.year
    row['month'] = date.month
    row['day'] = date.day
    row['week'] = date.week

# Process the ratings
def process_rating(row, rating_attribute='rating'):
    '''Converts an empty string to a None'''
    if row[rating_attribute] == '':
        row[rating_attribute] = None