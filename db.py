from pymongo import MongoClient

conn= MongoClient("mongodb://localhost:27017")

db=conn["student_management_system"]

# db_=db["student"]

# db2_=db["subject"]

# db3_=db["Students_Subject"]

# db4_=db["teachers"]