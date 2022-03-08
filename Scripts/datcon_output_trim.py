import pandas as pd
import numpy as np
import glob
import os

# get names of all csv files in current dir
path = ""
files = glob.glob(path + "*.csv")
# if output folder doesnt exist, create it
if not os.path.exists("datcon_output_trim"):
    os.mkdir("datcon_output_trim")
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
    # create new dataframe with only the following selected, top empty row removed
    selection = df.loc[1:,["GPS:Long", "GPS:Lat", "GPS:heightMSL", "GPS:Date", "GPS:Time"]].copy()
    # total rows in selection
    num_rows = len(selection.index)
    # count number of null cells
    stats_dict["Longitude Nulls"] = selection["GPS:Long"].isnull().sum()
    stats_dict["Latitude Nulls"] = selection["GPS:Lat"].isnull().sum()
    stats_dict["Height Nulls"] = selection["GPS:heightMSL"].isnull().sum()
    stats_dict["Date Nulls"] = selection["GPS:Date"].isnull().sum()
    stats_dict["Time Nulls"] = selection["GPS:Time"].isnull().sum()
    # count number of zeros present in columns
    # sometimes FLYXXX.DAT files contain cells with large number of zeros
    try:
        stats_dict["Longitude Zeros"] = selection["GPS:Long"].value_counts()[0]
    except:
        stats_dict["Longitude Zeros"] = 0 
    try:
        stats_dict["Latitude Zeros"] = selection["GPS:Lat"].value_counts()[0]
    except:
        stats_dict["Latitude Zeros"] = 0
    try:
        stats_dict["Height Zeros"] = selection["GPS:heightMSL"].value_counts()[0]
    except:
        stats_dict["Height Zeros"] = 0
    try:
        stats_dict["Date Zeros"] = selection["GPS:Date"].value_counts()[0]
    except:
        stats_dict["Date Zeros"] = 0
    try:
        stats_dict["Time Zeros"] = selection["GPS:Time"].value_counts()[0]
    except:
        stats_dict["Time Zeros"] = 0
    # convert dataframe to numpy array
    selection_array = (selection["GPS:Long"].to_numpy())
    # remove zeros
    remove_zeros = selection_array[selection_array != 0] 
    # remove nan value
    remove_nan = remove_zeros[np.logical_not(np.isnan(remove_zeros))]
    # find minmia and maxima values
    minima = np.min(remove_nan)
    maxima = np.max(remove_nan)
    print(minima, maxima)
    range = maxima - minima
    if range > 1:
        long_warning = True
    else:
        long_warning = False
    # create log file to make identifing poor quality FLYXXX.DAT files easier
    
    with open("datcon_output_trim/datcon_output_trim_log.txt", "a") as f:
        print(files[x], file = f)
        print("--------------------", file = f)
        for key in stats_dict:
            print(key, " : ", stats_dict[key], file = f)
        print("total rows : ", num_rows, file = f)
        if long_warning:
            print("WARNING large change in longitude", file = f)
            print("longitude range ")
        print("--------------------", file = f)
        
    # output selections to csv for QGIS
    #selection.to_csv(f"datcon_output_trim/trim_{files[x]}")
