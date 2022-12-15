import pymongo
from pymongo import MongoClient


# initial connection
cluster = MongoClient("mongodb+srv://apaige161:nIEacKRy0zP2N1eI@cluster0.xgz1dnl.mongodb.net/?retryWrites=true&w=majority")

#define database and collection
db = cluster["test"]
collection = db["players"]

post1 = {"_id": 0, "name": "Alex", "score": 5}
post2 = {"_id": 1, "name": "Alex", "score": 5}
post3 = {"_id": 2, "name": "Alex", "score": 5}

# add one
# collection.insert_one(post)

# add many
# collection.insert_many([post1, post2, post3])

# find
results = collection.find({"_id":"0"})
print(results)