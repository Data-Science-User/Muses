# Libraries
import json, requests
import pandas as pd
import sqlite3 as lite

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

## Rearrange Dataset before storing to MYSQL database
data_norm = data_norm[['id', 'name', 'publication_date', 'locations', 'company', 'categories','levels', 'tags',
       'type','model_type', 'short_name', 'contents', 'refs']]


data_norm.to_sql(db, con, flavor=None, schema=None, if_exists='fail', index=True,
                 index_label=None, chunksize=None, dtype=None)
## Make SQL Database
con = lite.connect('db.db')
cur = con.cursor()

cur.execute("CREATE TABLE db("
            "ID INT, Name TEXT, Publication_Date TEXT, Location TEXT, Company TEXT, Categories TEXT, Levels TEXT, "
            "Type TEXT, Model_Type TEXT, Tags TEXT, Short_name TEXT, Contents TEXT, Refs TEXT)")
df = pandas.DataFrame({'Identity': range(10), 'Name': range(5,10), 'Publication_Date': range(10,15),
                       'Location': range(5,10),'Company': range(10,15), 'Categories': range(5,10),
                       'Levels': range(5,10),'Type': range(10),'Model_Type': range(10),'Tags': range(5,10),
                       'Short_name': range(10,15), 'Contents': range(100),'Refs': range(50),}, dtype=numpy.int32)

cur.executemany("INSERT INTO Cars (Id, Price, Name) VALUES(?,?,?)",
                list(df[['Identity', 'Value', 'Name']].to_records(index=False)))

query ="SELECT * from The_Muse"
cur.execute(query)
rows= cur.fetchall()
for row in rows:
    print (row)