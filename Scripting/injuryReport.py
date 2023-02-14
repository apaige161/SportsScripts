
# Python program to read
# json file
  
import csv
import json

from pymongo import MongoClient

def getInjuryReport(sport):
    # initial connection
    cluster = MongoClient("mongodb+srv://apaige161:nIEacKRy0zP2N1eI@cluster0.xgz1dnl.mongodb.net/?retryWrites=true&w=majority")
    print('Connected to DB')
    #define database and collection
    db = cluster["test"]
    collection = db["injuredplayers"]

    injuryReport = []
  
    ############# Read game data
    # Opening JSON file
    # print('Reading game Data')
    # f = open('Scripting/json/gameData_'+ sport+'.json')

    # # returns JSON object as 
    # # a dictionary
    # gameData = json.load(f)

    # # Closing file
    # f.close()

    ############# Read player Data
    csvFilePath = 'Scripting/csv/Player_'+ sport+'.csv'

    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 
        print('Reading player data')

        #convert each csv row into python dict
        for dict in csvReader: 
            if (dict['InjuryStatus'] != 'Healthy'):
                dict['Sport'] = sport
                #add this python dict to json array
                injuryReport.append(dict)

                # collection.insert_one(dict) # <-- run this at start of the season
                collection.update_one({'Player': dict['Player']}, {"$set": {'InjuryStatus': dict['InjuryStatus']}})
                dict['_id'] = '' 
    print('Updated DB for', sport)
    # write players to bet on to csv
    with open('Scripting/json/injuryReport_'+ sport+'.json', 'w', encoding='utf-8') as f:
        json.dump(injuryReport, f, ensure_ascii=False, indent=4)
    print('Updated JSON for', sport)

# getInjuryReport("basketball")
# getInjuryReport("football")
# getInjuryReport("hockey")