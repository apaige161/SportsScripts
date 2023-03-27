import json
from pymongo import MongoClient



def writePlayersToDb(sport):
    # Open JSON file 
    with open('Scripting/json/BirthdayPlayerPlusStatsAndInjury_'+sport+'.json', "r") as birthdayFile:
        playerList = json.load(birthdayFile)

    cluster = MongoClient("mongodb+srv://apaige161:nIEacKRy0zP2N1eI@cluster0.xgz1dnl.mongodb.net/?retryWrites=true&w=majority")
    print('Connected to DB')
    #define database and collection
    db = cluster["test"]
    collection = db["players"]

    for i in range(len(playerList)):

        collection.update_one(
        {'Player': playerList[i]['Player']}, 
        {"$set": 
            {
                'Stats': playerList[i]['Stats'], 'InjuryStatus': playerList[i]['InjuryStatus'], 
                'TeamInjuryReport': playerList[i]['TeamInjuryReport']
            }
        })
        # collection.insert_one(playerList[i])
    print('DB done:', sport)

# writePlayersToDb('basketball')
# writePlayersToDb('hockey')