#!/bin/bash

# install download manager
sudo apt install aria2

aria2c -x 4 https://archive.org/download/nycTaxiTripData2013/trip_fare.7z
aria2c -x 8 https://archive.org/download/nycTaxiTripData2013/trip_data.7z

# decompress data
7z x trip_data.7z
7z x trip_fare.7z