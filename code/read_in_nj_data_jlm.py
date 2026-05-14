

# Import packages
import pandas as pd
import requests
from io import StringIO

API_URL = "https://zelma.ai/api/data/3.0?"
PARAMS = {"state": "NJ", "year": "2024"}

# Get the data using parameters
response = requests.get(API_URL, params = PARAMS, timeout=(3.05, 10))

# Get the data using the full code
# response = requests.get("https://zelma.ai/api/data/3.0?state=NJ&year=2024", timeout=(3.05, 10))

# read it into a data frame
df = pd.read_csv(StringIO(response.text), dtype=object)

# keep only All Students
df = df[df["StudentGroup"] == "All Students"]

# save to computer
df.to_csv("nj_2024.csv", index=False)

# Next steps
 # figure out how to handle when file not returned (e.g. Covid years)
 # get this in a loop to download multiple years (or could remove the year qualifier)
 # download for mutliple states
 # work through percentile calculation
