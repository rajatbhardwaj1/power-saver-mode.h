import psycopg2
import os
import random 
# function to get all images in a directory and its subdirectories

import pandas as pd 

df = pd.read_csv('/home/project/power-saver-mode.h/data/Person.csv')


string_list1 = df.iloc[:, 0].astype(str).tolist()

sizeofker = len(string_list1)

conn = psycopg2.connect(database="dbmsproject", user="postgres", password="", host="localhost", port="5432")
cur = conn.cursor()

friends = set()
for i in range(30000):
    rand1 = random.randint(0,sizeofker-1)
    rand2 = random.randint(0,sizeofker-1)
    if rand1 == rand2:
        continue
    if rand1 > rand2 :
        rand3 = rand1
        rand1 = rand2
        rand2 = rand3 
    friends.add((string_list1[rand1],string_list1[rand2]))


for str1,str2 in friends:
    cur.execute("insert into friends values(%s,%s);", (str1,str2))
conn.commit()
cur.close()
conn.close()
