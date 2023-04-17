import psycopg2
import os
import random 
# function to get all images in a directory and its subdirectories

import pandas as pd 

df = pd.read_csv('data/Person_Belongsto_Group.csv')
df1 = pd.read_csv('captions_csv.csv')


# extract the first column and convert it to a list of strings
string_list1 = df.iloc[:, 0].astype(str).tolist()
string_list2 = df.iloc[:, 1].astype(str).tolist()
string_listcaption1 = df1.iloc[:, 2].astype(str).tolist()
print(len(string_list1) , len(string_list2))
sizeofker = len(string_list1)
sizeofcap = len(string_listcaption1)

def get_images(directory):  # sourcery skip: for-append-to-extend
    images = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
                images.append(os.path.join(dirpath, filename))
    return images
main_directory = '/home/rajat/Desktop/COURSES/COL362/Assignments/Project/power-saver-mode.h/-'
images = get_images(main_directory)

# print(images)
print(len(images))

conn = psycopg2.connect(database="dbmsproject", user="postgres", password="", host="localhost", port="5432")
cur = conn.cursor()
#creation of table
cur.execute("CREATE TABLE Post(postID char(8) PRIMARY KEY,  image bytea,  caption varchar,  postedBy char(10),  belongsToGroups char(8));")
ID = 1 
for image in images:
    curid = str(ID)
    curid = "P" + (7 - len(curid))*"0" + curid
    with open(image, "rb") as f:
        image_data = f.read()
        random_number = random.randint(1, 10)
        random_number1 = random.randint(0, sizeofker-1)
        random_numbercap = random.randint(0, sizeofcap-1)
        if random_number > 7: #person and group
            per = string_list1[random_number1]
            grp = string_list2[random_number1]
            cap = string_listcaption1[random_numbercap]
            cur.execute("INSERT INTO Post (postID, image ,caption,postedby , belongsToGroups ) VALUES (%s, %s, %s,%s,%s);", (curid, image_data ,cap , per, grp))
        
        else :
            per = string_list1[random_number1]
            grp = string_list2[random_number1]
            cap = string_listcaption1[random_numbercap]
            cur.execute("INSERT INTO Post (postID, image ,caption,postedby  ) VALUES (%s, %s,%s,%s);", (curid, image_data ,cap , per))
        
    ID += 1 
    if ID % 1000 == 0:
        print(f"{ID} of 18845 images added")
cur.execute("SELECT image FROM post WHERE postid = %s;", ("P0000040",))
conn.commit()
image_data = cur.fetchone()[0]
with open("test_output11.png", "wb") as f:
    f.write(image_data)
cur.close()
conn.close()
