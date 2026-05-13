import pandas as pd
import requests
from io import StringIO
import warnings
warnings.filterwarnings("ignore")  # suppresses the OpenSSL warning
import time

## PART 1: RETRIEVE DATA FROM API AND COMBINE INTO SINGLE DF ##

url_base = "https://zelma.ai/api/data/3.0?state=NJ&year="
yr_text = list(range(2015, 2026)) # list of years to loop through -- starting in 2015 for simplicity

dfs = list() # empty list to store dfs for each year

for yr in yr_text:
    url = url_base + str(yr)
    max_retries = 3  # Number of retry attempts
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)  # Add timeout to prevent hanging
            response.raise_for_status()  # Raise an exception for bad status codes (e.g., 404, 500)
            df = pd.read_csv(StringIO(response.text), dtype=object)
            df["TestYear"] = yr  # Add a column to indicate the year of the data
            dfs.append(df)
            break  # Success, exit retry loop
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for year {yr}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
            else:
                print(f"Failed to fetch data for year {yr} after {max_retries} attempts.")
    time.sleep(1)  # Delay between years to be polite to the server

df = pd.concat(dfs, ignore_index=True)

## PART 2: DROP UNNECESSARY ROWS & COLUMNS ##

# Drop science rows
df = df[df["Subject"] != "sci"] 

# Name columns to drop
drop1 = ["AssmtType", # all "regular"
           "DistLocale",
           "AvgSS_SD",
           "ProficiencyCriteria", #all levels 4-5
           "Version"]

drop2 = df.filter(like="Flag_").columns.tolist() 

drop3 = [col for col in df.columns if col.startswith("Lev")]
# drop3 = df.filter(regex = "^Lev").columns.tolist() ## Runs very slowly

cols_to_drop = drop1 + drop2 + drop3

# Drop columns
df.drop(columns=cols_to_drop, inplace=True)

# Save as CSV for future use
df.to_csv("nj_data_2015_2025.csv", index=False)