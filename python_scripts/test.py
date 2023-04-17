import pandas as pd

# read the CSV file into a pandas DataFrame
# df = pd.read_csv('data/Person_Belongsto_Group.csv')

# # extract the first column and convert it to a list of strings
# string_list1 = df.iloc[:, 0].astype(str).tolist()
# string_list2 = df.iloc[:, 1].astype(str).tolist()

# print the string list
p = set()
p.add((1,2))
p.add((1,2))
for str1 , str2 in p :
    print(str1)
    print(str2)
print(p)