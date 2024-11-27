import sqlite3
import numpy as np
from sklearn.cluster import KMeans

# Connect to the SQLite3 database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Query the database to get the "long" and "lat" columns
print("Loading database.")
c.execute("SELECT long, lat FROM data")
data = c.fetchall()

# Convert the data to a NumPy array
X = np.array(data)

# Perform KMeans clustering with 20 clusters
print("Fitting the model.")
kmeans = KMeans(n_clusters=20, random_state=0)
kmeans.fit(X)

# Get the cluster labels
labels = kmeans.labels_
centers = kmeans.cluster_centers_

# Create a new column 'cluster' in the database and store the cluster labels
print("Storing cluster labels in the database.")
# c.execute("ALTER TABLE data ADD COLUMN cluster INTEGER")
for i, label in enumerate(labels):
    c.execute("UPDATE data SET cluster = ? WHERE rowid = ?", (int.from_bytes(label, byteorder='little', signed=False), i+1))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Clustering complete. Cluster IDs stored in the 'cluster' column of the database.")

# Save the cluster boundaries
np.save('cluster_centers.npy', centers)
np.save('cluster_labels.npy', labels)
