# Download the dataset

Source: https://www.gbif.org/dataset/4bf1cca8-832c-4891-9e17-7e7a65b7cc81
GBIF.org (25 September 2019) GBIF Occurrence Download https://doi.org/10.15468/dl.kvdukn

Download Information:
```
DOI: https://doi.org/10.15468/dl.kvdukn (may take some hours before being active)
Creation Date: 07:15:05 25 September 2019
Records included: 10153635 records from 1 published datasets
Compressed data size: 868.8 MB
Download format: simple tab-separated values (TSV)

Birdata is your gateway to BirdLife Australia data including the Atlas of
Australian Birds and Nest record scheme. You can use Birdata to draw bird
distribution maps and generate bird lists for any part of the country. You can
also join in the Atlas and submit survey information to this important
environmental database.

Please note that Birdlife data is available under a non-commercial license and
consultants should contact Birdlife directly to arrange access to full
resolution records for commercial purposes.
```

There is no need to unpack the zip file as it can directly be read by Pandas as below. Beware that the dataset takes up around ~9GB in memory:
```
>>> import pandas as pd
>>> df = pd.read_csv('0003827-190918142434337.zip', compression='zip', sep='\t')
sys:1: DtypeWarning: Columns (9,10,49) have mixed types. Specify dtype option on import or set low_memory=False.
>>> df.head()
       gbifID                            datasetKey                          occurrenceID   kingdom    phylum class  ... recordedBy typeStatus establishmentMeans           lastInterpreted mediaType issue
0  1624000000  4bf1cca8-832c-4891-9e17-7e7a65b7cc81  218a09fd-755f-43ab-b89e-58cabee4e445  Animalia  Chordata  Aves  ...        NaN        NaN                NaN  2019-09-20T17:11:58.801Z       NaN   NaN
1  1624000001  4bf1cca8-832c-4891-9e17-7e7a65b7cc81  b8635b28-0da7-40e9-a3fd-5d61f67ff2e5  Animalia  Chordata  Aves  ...        NaN        NaN                NaN  2019-09-20T17:11:59.793Z       NaN   NaN
2  1624000002  4bf1cca8-832c-4891-9e17-7e7a65b7cc81  29ff345a-4bf3-49df-887c-6a52fb86cdf7  Animalia  Chordata  Aves  ...        NaN        NaN                NaN  2019-09-20T17:11:58.797Z       NaN   NaN
3  1624000003  4bf1cca8-832c-4891-9e17-7e7a65b7cc81  c3d47442-e3cc-458a-818f-0814e5a0c72a  Animalia  Chordata  Aves  ...        NaN        NaN                NaN  2019-09-20T17:12:02.806Z       NaN   NaN
4  1624000004  4bf1cca8-832c-4891-9e17-7e7a65b7cc81  1a6871cc-c83a-4538-a2c5-1761d543d1cf  Animalia  Chordata  Aves  ...        NaN        NaN                NaN  2019-09-20T17:11:58.400Z       NaN   NaN

[5 rows x 50 columns]
>>> df.shape[0]
9853231
>>> df.columns
Index(['gbifID', 'datasetKey', 'occurrenceID', 'kingdom', 'phylum', 'class',
       'order', 'family', 'genus', 'species', 'infraspecificEpithet',
       'taxonRank', 'scientificName', 'verbatimScientificName',
       'verbatimScientificNameAuthorship', 'countryCode', 'locality',
       'stateProvince', 'occurrenceStatus', 'individualCount',
       'publishingOrgKey', 'decimalLatitude', 'decimalLongitude',
       'coordinateUncertaintyInMeters', 'coordinatePrecision', 'elevation',
       'elevationAccuracy', 'depth', 'depthAccuracy', 'eventDate', 'day',
       'month', 'year', 'taxonKey', 'speciesKey', 'basisOfRecord',
       'institutionCode', 'collectionCode', 'catalogNumber', 'recordNumber',
       'identifiedBy', 'dateIdentified', 'license', 'rightsHolder',
       'recordedBy', 'typeStatus', 'establishmentMeans', 'lastInterpreted',
       'mediaType', 'issue'],
      dtype='object')
>>> df[[''decimalLatitude', 'decimalLongitude']]
  File "<stdin>", line 1
    df[[''decimalLatitude', 'decimalLongitude']]
                        ^
SyntaxError: invalid syntax
>>> df[['species','decimalLatitude', 'decimalLongitude', 'eventDate']].head()
               species  decimalLatitude  decimalLongitude             eventDate
               0  Calidris ruficollis        -32.88222         151.79140  2000-02-05T00:00:00Z
               1  Calidris ruficollis        -34.69778         138.48030  2000-03-20T00:00:00Z
               2  Calidris ruficollis        -35.37039         139.13690  2000-03-16T00:00:00Z
               3  Calidris ruficollis        -16.56589         145.51011  1999-10-11T00:00:00Z
               4  Calidris ruficollis        -12.36278         130.86860  2000-03-04T00:00:00Z
```
But only around 4.7GB if only keeping the columns `['species','decimalLatitude', 'decimalLongitude', 'eventDate']`.
