import pandas as pd
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

    num_rows = len(selection.index)

    if selection["GPS:Long"].notnull().values.any():
        stats_dict["Longitude Zeros"] = selection["GPS:Long"].value_counts()[0]
        stats_dict["Longitude Nulls"] = selection["GPS:Long"].isnull().sum()
        
    if selection["GPS:Lat"].notnull().values.any():
        stats_dict["Latitude Zeros"] = selection["GPS:Lat"].value_counts()[0]
        stats_dict["Latitude Nulls"] = selection["GPS:Lat"].isnull().sum()
    
    if selection["GPS:heightMSL"].notnull().values.any():
        stats_dict["Height Zeros"] = selection["GPS:heightMSL"].value_counts()[1]
        stats_dict["Height Nulls"] = selection["GPS:heightMSL"].isnull().sum()
    

    if selection["GPS:Date"].notnull().values.any():
        stats_dict["Date Zeros"] = selection["GPS:Date"].value_counts()[0]
        stats_dict["Date Nulls"] = selection["GPS:Date"].isnull().sum()
    
    if selection["GPS:Time"].notnull().values.any():
        stats_dict["Time Zeros"] = selection["GPS:Time"].value_counts()[0]
        stats_dict["Time Nulls"] = selection["GPS:Time"].isnull().sum()
    



    print(stats_dict)

    print(num_rows)

    selection.info()




    # selection.to_csv(f"datcon_output_trim/trim_{files[x]}")
