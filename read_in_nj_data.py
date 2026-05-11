import pandas as pd
import requests
from io import StringIO
import warnings
warnings.filterwarnings("ignore")  # suppresses the OpenSSL warning

url = "https://zelma.ai/api/data/3.0?state=NJ&year=2025"
response = requests.get(url)
df = pd.read_csv(StringIO(response.text), dtype=object)

print(df.shape)    # how many rows and columns
print(df.head())   # first 5 rows
print(df.columns.tolist())  # full list of column names