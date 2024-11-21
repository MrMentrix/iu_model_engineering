import sqlite3
import pandas as pd

conn = sqlite3.connect("data.db")
df = pd.read_sql("SELECT * FROM data", conn)

clusters = {}

for cluster in df["cluster"].unique():
    sub_df = df[df["cluster"] == cluster]
    clusters[cluster] = len(sub_df)

sorted_clusters = {k: clusters[k] for k in sorted(clusters, key=clusters.get, reverse=True)}

print(sorted_clusters)

### Results
# np.int64(0): 2241440
# np.int64(7): 2200268
# np.int64(6): 1542490
# np.int64(9): 980238
# np.int64(2): 493910
# np.int64(12): 433228
# np.int64(3): 265872
# np.int64(16): 237786
# np.int64(1): 227436
# np.int64(11): 123774
# np.int64(13): 95952
# np.int64(4): 82966
# np.int64(17): 77832
# np.int64(15): 23046
# np.int64(19): 13126
# np.int64(5): 8840
# np.int64(10): 8592
# np.int64(18): 7684
# np.int64(8): 2142
# np.int64(14): 2032
