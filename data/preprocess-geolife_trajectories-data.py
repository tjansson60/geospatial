#!/usr/bin/env python

import os
import multiprocessing
import glob
import tqdm
import pandas as pd

INPUT_FILES       = glob.glob('Geolife Trajectories 1.3/Data/*/Trajectory/*.plt')
OUTPUT_FILE       = 'geolife_trajectories_1_3.parquet'
OUTPUT_FILE_SMALL = 'small.parquet'
SMALL_NUM_TRIPS   = 100


def process_plt(input_tupple, verbose=False):
    '''
    Processes a plt file from the Geolife Trajectories 1.3 dataset:
    https://www.microsoft.com/en-us/download/details.aspx?id=52367&from=http%3A%2F%2Fresearch.microsoft.com%2Fen-us%2Fdownloads%2Fb16d359d-d164-469e-9fd4-daa38f2b2e13%2F

    PLT format:
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
    filename, tripId, userId = input_tupple

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

    # Add tripId and userId
    df['tripId'] = tripId
    df['userId'] = userId

    if verbose:
        print(df)

    return df


if __name__ == '__main__':

    # Testing a single file
    process_plt((INPUT_FILES[0], 'tripId1', 'userId1'), verbose=True)

    # Process all the file in parallel. This takes around 22 seconds to process all 18670 and write a single file with
    # 24.876.978 rows.
    mp_pool = multiprocessing.Pool()
    mp_input_list = []
    for filename in INPUT_FILES:
        id1 = os.path.basename(filename).split('.plt')[0]
        userId = filename.split('/')[2]
        tripId = f'{userId}_{id1}'
        mp_input_list.append((filename, tripId, userId))
    df_list = list(tqdm.tqdm(mp_pool.imap_unordered(process_plt, mp_input_list), total=len(mp_input_list)))

    # Combine all the files together,
    df = pd.concat(df_list, ignore_index=True)
    print(df.shape[0])
    print(df.dtypes)
    print(df)

    # Save the data to parquet format
    print(f'Saving data to parquet format: {OUTPUT_FILE}')
    # Brotli compression is a bit slower to write, but is much smaller. See:
    # https://tech.jda.com/efficient-dataframe-storage-with-apache-parquet/
    # Snappy (default): 474 MB
    # Gzip: 297 MB
    # Brotli: 217 MB
    df.to_parquet(OUTPUT_FILE, compression='brotli')

    # Only select the X trips with most points
    tripIds = df.groupby('tripId')['datetime'].count().sort_values(ascending=False).head(SMALL_NUM_TRIPS).index.tolist()
    df_small = df[df.tripId.isin(tripIds)].copy()
    print(f'Saving data to parquet format: {OUTPUT_FILE_SMALL}')
    df_small.to_parquet(OUTPUT_FILE_SMALL, compression='brotli')
