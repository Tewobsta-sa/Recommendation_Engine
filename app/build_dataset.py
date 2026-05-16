import requests
import pandas as pd

API_URL = (
    "http://localhost:5050/api/training-data"
)

# STEP 1
# Fetch API response
response = requests.get(API_URL)

# STEP 2
# Convert JSON payload
payload = response.json()

# STEP 3
# Extract actual training rows
training_rows = payload["data"]

# STEP 4
# Convert to DataFrame
df = pd.DataFrame(training_rows)

# STEP 5
# Save CSV
df.to_csv(
    "data/training_dataset.csv",
    index=False
)

print("Dataset created successfully")
print(df.head())