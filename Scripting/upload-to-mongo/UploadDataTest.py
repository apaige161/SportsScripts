from .player import Player
from pymongo import MongoClient

def initTestData():
    testPlayerChris = Player("Christian Fischer", "RW", "ARI", "04/15", "04/13/23", "Healthy")
    testPlayerOliver = Player("Oliver Bjorkstrand", "RW", "SEA", "04/10", "04/13/23", "Healthy")

    return {testPlayerChris, testPlayerOliver}

def getDatabase():
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['test']
  
if __name__ == "__main__":   
    testData = initTestData()
    db = getDatabase()
    playerCollection = db['players']

    documentsToInsert = []
    for player in testData:
        documentsToInsert.append(player.__dict__)

    playerCollection.insert_many(documentsToInsert)