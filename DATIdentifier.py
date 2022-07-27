import pandas as pd
import numpy as np
import glob
import os

# get names of all csv files in current dir
path = ""
files = glob.glob(path + "*.csv")
# if output folder doesnt exist, create it
if not os.path.exists("DATIdentifierOUT"):
    os.mkdir("DATIdentifierOUT")
# dictionary for statistics generated
stats_dict = {
    "Longitude Zeros": 0,
    "Longitude Nulls": 0,
    "Latitude Zeros": 0,
    "Latitude Nulls": 0,
    "Height Zeros": 0,
    "Height Nulls": 0,
    "Date Zeros": 0,
    "Date Nulls": 0,
    "Time Zeros": 0,
    "Time Nulls": 0
}
# loop through all csv files found in current dir
for x in range(len(files)):
    # read csv into dataframe
    df = pd.read_csv(files[x], low_memory=False)
    # total rows in df
    num_rows = len(df.index)
    # count number of null cells
    stats_dict["Longitude Nulls"] = df["GPS:Long"].isnull().sum()
    stats_dict["Latitude Nulls"] = df["GPS:Lat"].isnull().sum()
    stats_dict["Height Nulls"] = df["GPS:heightMSL"].isnull().sum()
    stats_dict["Date Nulls"] = df["GPS:Date"].isnull().sum()
    stats_dict["Time Nulls"] = df["GPS:Time"].isnull().sum()
    # count number of zeros present in columns
    # sometimes FLYXXX.DAT files contain cells with large number of zeros
    try:
        stats_dict["Longitude Zeros"] = df["GPS:Long"].value_counts()[0]
    except:
        stats_dict["Longitude Zeros"] = 0 
    try:
        stats_dict["Latitude Zeros"] = df["GPS:Lat"].value_counts()[0]
    except:
        stats_dict["Latitude Zeros"] = 0
    try:
        stats_dict["Height Zeros"] = df["GPS:heightMSL"].value_counts()[0]
    except:
        stats_dict["Height Zeros"] = 0
    try:
        stats_dict["Date Zeros"] = df["GPS:Date"].value_counts()[0]
    except:
        stats_dict["Date Zeros"] = 0
    try:
        stats_dict["Time Zeros"] = df["GPS:Time"].value_counts()[0]
    except:
        stats_dict["Time Zeros"] = 0
    # convert dataframe to numpy array
    long_array = (df["GPS:Long"].to_numpy())
    lat_array = (df["GPS:Lat"].to_numpy())
    # remove zeros
    long_remove_zeros = long_array[long_array != 0] 
    lat_remove_zeros = lat_array[lat_array != 0] 
    # remove nan value
    long_remove_nan = long_remove_zeros[np.logical_not(np.isnan(long_remove_zeros))]
    lat_remove_nan = lat_remove_zeros[np.logical_not(np.isnan(lat_remove_zeros))]
    # reset warning flags
    long_warning = False
    lat_warning = False
    # if numpy array is not empty
    if long_remove_nan.size != 0:
        # find minmia and maxima values
        long_minima = np.min(long_remove_nan)
        long_maxima = np.max(long_remove_nan)
        # calculate range
        long_range = long_maxima - long_minima
        # set warning if range is large
        if long_range > 1:
            long_warning = True
    if lat_remove_nan.size != 0:
        lat_minima = np.min(lat_remove_nan)
        lat_maxima = np.max(lat_remove_nan)
        lat_range = lat_maxima - lat_minima
        if lat_range > 1:
            lat_warning = True
    # create log file to make identifing poor quality FLYXXX.DAT files easier
    with open("DATIdentifierOUT/DIOutput.txt", "a") as f:
        print(files[x], file = f)
        print("--------------------", file = f)
        for key in stats_dict:
            print(key, " : ", stats_dict[key], file = f)
        print("total rows : ", num_rows, file = f)
        if long_warning:
            print("WARNING large change in longitude", file = f)
            print("longitude range : ", long_range, file = f)
        if lat_warning:
            print("WARNING large change in latitude", file = f)
            print("longitude range : ", lat_range, file = f)
        print("--------------------", file = f)

