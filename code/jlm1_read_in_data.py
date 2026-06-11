

# Import packages
import pandas as pd
import requests
from io import StringIO
import time

# Set api url
API_URL = "https://zelma.ai/api/data/3.0"

# Set states and years to loop through
STATES = ["NJ", "NY", "MI", "MA"]
YEARS = range(2024, 2026)
MAX_RETRIES = 3 # number of times to retry on a timeout

all_dataframes = []

for state in STATES:
    print(f"\n---Processing State: {state} ---")

    for year in YEARS:

        PARAMS = {"state": state, "year": str(year)}

        print(f"Fetching data for {state} ({year})...")

        for attempt in range(MAX_RETRIES):

            try:
                
                # Get the data using parameters
                response = requests.get(API_URL, params = PARAMS, timeout=(3.05, 20))

                # trigger an error if status code is 400, 404, 500, etc.
                response.raise_for_status()

                # if code reaches here, data exists (status code 200)

                # read it into a data frame
                df = pd.read_csv(StringIO(response.text), dtype=object)

                # keep only All Students
                df = df[df["StudentGroup"] == "All Students"]

                # append to all_dataframes
                all_dataframes.append(df)
                print(f"Successfully loaded {state} ({year})")
                break # break loop and move to next year


            except requests.exceptions.HTTPError as err:

                if err.response.status_code == 404:
                    print(f" Data not found (404) for {year}. Skipping to next year")
                    break
                else:
                    print(f"Server returned an HTTP error: {err}")
                    break

            except requests.exceptions.RequestException as err:
                print(f"Network connection error occured: {err}")

        else:
            print(f"Failed to fetch data for {state} ({year}) after {MAX_RETRIES} attempts.")

        time.sleep(1)

print("\n Combining all datasets")

# ADJUSTED CODE BELOW TO MENTION THE PARQUET FILE. WILL NEED TO QA LATER.
# ALSO, NEED TO ADJUST TO SAVE TO THE DATA FOLDER. I DON'T THINK THAT HAPPENS NOW.

if all_dataframes: 

    # concatenate list of dataframes into one large dataframe
    master_df = pd.concat(all_dataframes, ignore_index=True)

    # save out to CSV file
    csv_filename = "data/all_states.csv"
    master_df.to_csv(csv_filename, index = False)
    print(f"Success! Saved {len(master_df)} rows to {csv_filename}")

    # save out to parquet file
    parquet_filename = "data/all_states.parquet"
    master_df.to_parquet(parquet_filename, engine = 'pyarrow')
    print(f"Success! Saved {len(master_df)} rows to {parquet_filename}")

else:
    print("No data was collected. Files were not saved.")

