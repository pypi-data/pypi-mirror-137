
from pydoc import describe
import pandas
from pandas.io.json import json_normalize

url="https://data.nasa.gov/resource/mc52-syum.json"
df= pandas.read_json(url)

DvsE=df.iloc[0,[0,8]]
print(DvsE)

