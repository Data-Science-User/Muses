# Libraries
import json, requests
import pandas as pd
from pandas.io.json import json_normalize

# Set URL
url = 'https://api-v2.themuse.com/jobs'

# For loop to
for i in range(100):
    data = json.loads(requests.get(
        url=url,
        params={'page': i}
    ).text)['results']

data_norm = pd.read_json(json.dumps(data))

# Dataset column names
data_norm.dtypes.index

# Parse out 'name' and unlist locations variable
data_norm.locations = data_norm.locations.apply(lambda x:
                                                x[0].get('name', '')
                                                if len(x) > 0 else ''
                                                )
# Convert publication_date variable to datetime64
data_norm.publication_date = pd.to_datetime(data_norm.publication_date)

# Subset and store data range and location into dataset object
df1 = data_norm[(data_norm['publication_date'] >= '2016-09-01') &
          (data_norm['publication_date'] <= '2016-09-30') &
          (data_norm['locations'] == 'New York City Metro Area')]

# Print frequency of job listing in New York City Metro Area from 2016-09-01 to 2016-09-30 compared to total frequency
print (len(df1.index) / len(data_norm.index))

# Print number of job listings in New York City Metro Area from 2016-09-01 to 2016-09-30
print (data_norm[(data_norm['locations'] == 'New York City Metro Area')  &
          (data_norm['publication_date'].between('2016-09-01', '2016-09-30'))])
