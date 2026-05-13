

# Example using pandas package
import pandas as pd
# Suggested: use dtype=object to avoid coercion
df = pd.read_csv("https://zelma.ai/api/data/3.0?year=2005", dtype=object)

# Example using requests package
import requests
response = requests.get("https://zelma.ai/api/data/3.0?year=2005")
with open("EDC-2005.csv", "w") as f:
    f.write(response.text)