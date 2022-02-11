import duckdb
import pandas as pd

def data_partition:
    ''' Remove error records through checking for missing values and unreasonable values in coordinate and speed
    '''
    df_trip = pd.read_csv("trip_data_5_week1.zip",parse_dates=["pickup_datetime","dropoff_datetime"])

    df_fare = pd.read_csv("trip_fare_5_week1.zip",parse_dates=["pickup_datetime"])

    # joining data
    join_query = " SELECT * FROM df_fare INNER JOIN df_trip USING (hack_license, medallion, pickup_datetime, vendor_id)"
    df = duckdb.query(join_query).df()
    df.head()


    # dropping store_and_fwd_flag columns because having too many missing value
    df = df.drop('store_and_fwd_flag', axis=1)

    # dropping rows with null dropoff_longitude or dropoff_latitude
    df = df[~df.dropoff_latitude.isnull()]
    df = df[~df.dropoff_longitude.isnull()]

    # dropping outlier location data, likely due to error
    longitude_limit = [-74.027, -73.85] # NYC coordinate
    latitude_limit = [40.67, 40.85]

    df = df[(df.pickup_longitude.between(longitude_limit[0], longitude_limit[1], inclusive=False))]
    df = df[(df.dropoff_longitude.between(longitude_limit[0], longitude_limit[1], inclusive=False))]
    df = df[(df.pickup_latitude.between(latitude_limit[0], latitude_limit[1], inclusive=False))]
    df = df[(df.dropoff_latitude.between(latitude_limit[0], latitude_limit[1], inclusive=False))]

    # removing trip where duration or distance = 0 
    df = df[df.trip_time_in_secs>0]
    df = df[df.trip_distance>0.0]

    # Let's create a feature to determine the speed of taxicabs.
    df['speed'] = df.trip_distance/(df.trip_time_in_secs/3600.0) # miles per hour

    # limit to trips with speed of 80 mph - highway speed limit in US, using threshold of 100 mph for buffer of error of measurement
    df = df[df.speed < 100.0]

    # saving clean and merged data
    compression_opts = dict(method='zip',

                            archive_name='df_5_week1.csv')  
    df.to_csv('df_5_week1.zip', index=False,

            compression=compression_opts)

if __name__ == '__main__':
    data_partition()