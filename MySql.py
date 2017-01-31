#!/usr/bin/env python

import pymysql

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Password1234!', db='The_Muse')

cur = db.cursor()
cur.execute("SELECT * FROM users")

print(cur.description)
print()

for row in cur:
    print(row)

cur.close()
conn.close()