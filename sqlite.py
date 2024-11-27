# as having multiple .csv files is a pain in the a-s-s, they will be turned into a single SQL database for easier use, more efficiency, and - why am I even explaining this? SQL >>> csv

import pandas as pd
from sqlalchemy import create_engine

# this could also be done using a dictionary walk - as long as we get all the .csv files.
all_paths = ["./data/data-apr14.csv", "./data/data-may14.csv", "./data/data-jun14.csv", "./data/data-jul14.csv", "./data/data-aug14.csv", "./data/data-sep14.csv"]
engine = create_engine('sqlite:///data.db') # connect to or create the database

for path in all_paths: # looping through all the .csv files
    df = pd.read_csv(path) # read the .csv file from the data folder
    df.dropna(inplace=True) # removing any null values

    # split "Date/Time" into a date and a time column, then drop "Date/Time column"
    df["date"] = pd.to_datetime(df["Date/Time"]).dt.date # extract the date from the "Date/Time" column
    df["time"] = pd.to_datetime(df["Date/Time"]).dt.time # extract the time from the "Date/Time column"
    df.drop('Date/Time', axis=1, inplace=True) # drop the "Date/Time" column as it now only as redundant information and is no longer needed
    df.drop("Base", axis=1, inplace=True) # Only repeats one value and is not needed

    df.rename(columns={"Lon": "long", "Lat": "lat", "Base": "base"}, inplace=True) # rename some columns to fit the overall lowercase naming

    # Convert lon and lat columns to float
    df['long'] = df['long'].astype(float)
    df['lat'] = df['lat'].astype(float)

    df.to_sql("data", engine, if_exists="append", index=False) # append the DataFrame to the SQL database