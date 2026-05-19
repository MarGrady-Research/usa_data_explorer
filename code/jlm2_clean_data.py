

# Import packages
import pandas as pd
import requests
from io import StringIO
import time

all_states = pd.read_parquet('all_states.parquet')




# This file will read in the all_states.parquet file, clean the data, 
# and then calculate percentiles (or that will happen in the next step)