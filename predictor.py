import sqlite3
import numpy as np
import pandas as pd


conn = sqlite3.connect("data.db")

df = pd.read_sql("SELECT * FROM data", conn)
df["time"] = pd.to_datetime(df["time"])
df["hour"] = df["time"].dt.hour
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

cluster_counts = dict(df['cluster'].value_counts().sort_index())
cluster_counts = dict(sorted(cluster_counts.items()))

MAX_CLUSTERS = 1

i = 0

while i < MAX_CLUSTERS and i < df["cluster"].nunique():

    average_per_hour = {}

    subset = df[df["cluster"] == i]

    date_diff = subset["date"].max() - subset["date"].min()
    for i in range(23):
        hour_set = subset[subset["hour"] == i]
        average_per_hour[i] = len(hour_set) / date_diff.days


    print(f"Cluster {i} averages: {average_per_hour}\n")
    i += 1