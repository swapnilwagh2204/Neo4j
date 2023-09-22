import pandas as pd

# Create a pandas DataFrame with 1 million records
df = pd.DataFrame({'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve'] * 200000,
                   'id': range(1000000)})

# Save the DataFrame to a CSV file
df.to_csv('name_id.csv', index=False)
