import psycopg2
import os
import random 
import pandas as pd 





conn = psycopg2.connect(
    database = 'group_19',
    host = '10.17.6.95',
    port = '5432',
    user = 'group_19',
    password = 'B0jzmL6aEhxI21'
)

cur = conn.cursor()

cur.execute("select kerberosid from person;")
ids = cur.fetchall()
# print(len(ids))
for id in ids:
    kid = id[0].strip()
    cur.execute("insert into passwords values(%s, %s);",(kid, kid))
    print(kid , kid)

conn.commit()
# cur.execute("select count(*) from passwords")
# pp = cur.fetchone()
# print(pp)

cur.close()
conn.close()
