import sqlite3
import numpy as np
import pandas as pd

def get_top(max_clusters=10):
    conn = sqlite3.connect("data.db")

    df = pd.read_sql(f"SELECT * FROM data WHERE date BETWEEN '2014-09-01' AND '2014-09-08'", conn)
    df["time"] = pd.to_datetime(df["time"])
    df["hour"] = df["time"].dt.hour
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d") # to allow later .max() - .min() calculation

    cluster_counts = dict(df["cluster"].value_counts().sort_index())
    cluster_counts = dict(sorted(cluster_counts.items(), key=lambda x: x[1]))

    i = 0
    total_tops = {}

    while i < max_clusters and i < df["cluster"].nunique():

        average_per_hour = {}

        subset = df[df["cluster"] == i]

        date_diff = subset["date"].max() - subset["date"].min()
        for j in range(23):
            hour_set = subset[subset["hour"] == j]
            average_per_hour[j] = len(hour_set) / date_diff.days

        total_tops[list(cluster_counts.keys())[i]] = average_per_hour
        i += 1
    
    return total_tops

total = get_top(3)

print(total)