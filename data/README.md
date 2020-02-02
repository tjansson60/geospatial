# Download the dataset

Source:
https://www.microsoft.com/en-us/download/details.aspx?id=52367&from=http%3A%2F%2Fresearch.microsoft.com%2Fen-us%2Fdownloads%2Fb16d359d-d164-469e-9fd4-daa38f2b2e13%2F

This GPS trajectory dataset was collected in (Microsoft Research Asia) Geolife project by 182 users in a period of over
three years (from April 2007 to August 2012). Last published: August 9, 2012.

Please cite the following papers when using this GPS dataset.
[1] Yu Zheng, Lizhu Zhang, Xing Xie, Wei-Ying Ma. Mining interesting locations and travel sequences from GPS
trajectories. In
Proceedings of International conference on World Wild Web (WWW 2009), Madrid Spain. ACM Press: 791-800.[2] Yu Zheng,
Quannan Li, Yukun Chen, Xing Xie, Wei-Ying Ma. Understanding Mobility Based on GPS Data. In Proceedings of
ACM conference on Ubiquitous Computing (UbiComp 2008), Seoul, Korea. ACM Press: 312-321.
[3] Yu Zheng, Xing Xie, Wei-Ying Ma, GeoLife: A Collaborative Social Networking Service among User, location and
trajectory.
Invited paper, in IEEE Data Engineering Bulletin. 33, 2, 2010, pp. 32-40.

## Process dataset
Download the zip file to the data folder and unzip. Run the `preprocess-geolife_trajectories-data.py` script to create a
single `data/geolife_trajectories_1_3.parquet` which is very efficent and only takes up 217 MB. 

```python
lat         lon            datetime  altitude_meters              tripId
0         39.947122  116.318730 2009-02-14 03:28:49         149.9616  20090214032849_023
1         39.947121  116.318705 2009-02-14 03:28:54         149.6568  20090214032849_023
2         39.947100  116.319021 2009-02-14 03:28:59         186.8424  20090214032849_023
3         39.947140  116.318876 2009-02-14 03:29:04         177.6984  20090214032849_023
4         39.947177  116.318921 2009-02-14 03:29:09         166.4208  20090214032849_023
...             ...         ...                 ...              ...                 ...
24876973  39.998200  116.455200 2007-10-08 15:04:48          50.0000  20071008015645_106
24876974  39.998383  116.454983 2007-10-08 15:04:58          50.0000  20071008015645_106
24876975  39.998350  116.454500 2007-10-08 15:05:11          50.0000  20071008015645_106
24876976  39.998117  116.454717 2007-10-08 15:05:26          48.0000  20071008015645_106
24876977  39.998100  116.454950 2007-10-08 15:05:53          49.0000  20071008015645_106

[24876978 rows x 5 columns]
Saving data to parquet format: data/geolife_trajectories_1_3.parquet
```                
