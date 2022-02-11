import pandas as pd

def data_partition:
    ''' Partition the compressed dataset to only select 1 week of data
    '''
    # fare dataset
    # read data for first week of May
    df_fare = pd.read_csv("trip_fare_5.csv",skipinitialspace=True) # remove space in column name
    df_fare['pickup_datetime'] = pd.to_datetime(df_fare['pickup_datetime'])

    # extract to csv
    df_fare.loc[df_fare["pickup_datetime"] <= "2013-05-07"]

    compression_opts = dict(method='zip',

                            archive_name='trip_fare_5_week1.csv')  

    df_fare.loc[df_fare["pickup_datetime"] < "2013-05-08"].to_csv('trip_fare_5_week1.zip', index=False,

            compression=compression_opts)  

    # trip dataset
    df_trip = pd.read_csv("trip_data_5.csv",skipinitialspace=True)

    df_trip['pickup_datetime'] = pd.to_datetime(df_trip['pickup_datetime'])

    compression_opts = dict(method='zip',

                            archive_name='trip_data_5_week1.csv')  

    df_trip.loc[df_trip["pickup_datetime"] < "2013-05-08"].to_csv('trip_data_5_week1.zip', index=False,

            compression=compression_opts)

if __name__ == '__main__':
    data_partition()
