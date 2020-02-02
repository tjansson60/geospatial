#!/usr/bin/env python

import os
import glob
import tqdm
import pandas as pd

OUTPUT_FILE = 'data/geolife_trajectories_1_3.parquet'


def process_plt(filename, tripId, verbose=False):
    '''
    Line 1...6 are useless in this dataset, and can be ignored. Points are described in following lines, one for each line.
    Field 1: Latitude in decimal degrees.
    Field 2: Longitude in decimal degrees.
    Field 3: All set to 0 for this dataset.
    Field 4: Altitude in feet (-777 if not valid).
    Field 5: Date - number of days (with fractional part) that have passed since 12/30/1899.
    Field 6: Date as a string.
    Field 7: Time as a string.
    Note that field 5 and field 6&7 represent the same date/time in this dataset. You may use either of them.

    '''
    df = pd.read_csv(
        filename,
        skiprows=6,
        names=['lat', 'lon', 'DELETE', 'altitude_feet', 'DELETE2', 'date', 'time']
    )

    # Convert to datetime
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

    # Convert altitude to meters
    df['altitude_meters'] = df['altitude_feet'] * 0.3048

    # Remove unwanted columns
    df.drop(columns=['DELETE', 'DELETE2', 'date', 'time', 'altitude_feet'], inplace=True)

    # Add a tripId
    df['tripId'] = tripId

    if verbose:
        print(df)

    return df


# Testing
process_plt(
    'data/Geolife Trajectories 1.3/Data/000/Trajectory/20090704042634.plt',
    '000_20090704042634',
    verbose=True)

files = glob.glob('data/Geolife Trajectories 1.3/Data/*/Trajectory/*.plt')
df_list = [None for f in files]
for filename in tqdm.tqdm(files):
    id1 = os.path.basename(filename).split('.plt')[0]
    id2 = filename.split('/')[3]
    tripId = f'{id1}_{id2}'

    df_single = process_plt(filename, tripId)
    df_list.append(df_single)

df = pd.concat(df_list, ignore_index=True)
print(df.shape[0])
print(df)

# Save the data to parquet format
print(f'Saving data to parquet format: {OUTPUT_FILE}')
df.to_parquet(OUTPUT_FILE)
