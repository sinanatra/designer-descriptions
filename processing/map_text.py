# adapted from my own script at https://github.com/sinanatra/image-tsne/blob/master/notebooks/metadata_umap.ipynb
import pandas as pd
import numpy as np
import altair as alt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
import umap.umap_ as umap
import os  

url = "./data.csv"
data = pd.read_csv(url)

data = data[data["text"].notna()]

selection = data["text"]

cv = CountVectorizer()

components = cv.fit_transform(selection)
components.shape

reducer = umap.UMAP(
    n_neighbors=15,  
    min_dist=0.1,    
    metric='cosine',  
    random_state=42   
)

pipe = Pipeline([
    ('scaling', StandardScaler()), 
    ('umap', reducer)  
])
embedding = pipe.fit_transform(components.toarray())

umap_positions = pd.DataFrame(embedding, columns=["x", "y"])

data_umap = pd.concat([data, umap_positions], axis = 1)

x_domain = [data_umap["x"].min(), data_umap["x"].max() ]
y_domain = [data_umap["y"].min(), data_umap["y"].max() ]
tx, ty = data_umap["x"].dropna(), data_umap["y"].dropna()
tx = (tx-np.min(tx)) / (np.max(tx) - np.min(tx))
ty = (ty-np.min(ty)) / (np.max(ty) - np.min(ty))

data_umap.to_csv('./umap.csv')  