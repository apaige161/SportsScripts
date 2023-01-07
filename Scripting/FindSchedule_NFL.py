import requests
import datetime as dt
from csv import DictReader 
import csv
from helper import getAdjustedBirthdays
import json
import pymongo
from pymongo import MongoClient

# read NFL player CSV and load it into a dict
    # https://blog.finxter.com/convert-csv-to-dictionary-in-python/

def compareBirthdayToNFLSchedule():
    # initial connection
    cluster = MongoClient("mongodb+srv://apaige161:nIEacKRy0zP2N1eI@cluster0.xgz1dnl.mongodb.net/?retryWrites=true&w=majority")
    print('Connected to DB')
    #define database and collection
    db = cluster["test"]
    collection = db["players"]

    print('reading player birthdays')

    sport = 'football'

    # Store all player data in a list of dictionaries
    with open("Scripting/csv/Player_football.csv", "r") as birthdayFile:
        playerList = [*csv.DictReader(birthdayFile)]
        
    getAdjustedBirthdays(playerList)

    # add week number to the end
    baseUrl = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week=' 

    playsNearBirthdayList:list = []

    # Get data for each week
    for i in range(18):
        week = i + 1
        print('***Week', week, '***')

        # Read games by week from API
        adjustedUrl = baseUrl + str(week)
        req = requests.get(adjustedUrl)
        statusCode = req.status_code

        if(statusCode != 200):
            print('Status Code: ', statusCode)
            quit()
        
        # convert data to JSON
        data = req.json()

        WeeklyList = data['events']
        
        # formattedDate = ''

        for i in range(len(WeeklyList)):
            game = WeeklyList[i]['shortName']
            Gamedate = WeeklyList[i]['date'].split("T")
            Gamedate = Gamedate[0]
            updatedDate = Gamedate.split('-')
            formattedDate = dt.datetime(int(updatedDate[0]),int(updatedDate[1]),int(updatedDate[2]))
            # convert date to string
            GameDay = formattedDate.strftime("%m/%d/%y")
            print(game + ' | Date: ' + GameDay)
            GameDay = formattedDate.strftime("%m/%d")
            
            # check if any player birthdays are on this day
            for x in range(len(playerList)):
                # print player if they play near their birthday /playerList[x]['Team'] in game
                if ( ((GameDay == playerList[x]['Birthday']) or (GameDay == playerList[x]['BirthdayMinusOne']) or 
                    (GameDay == playerList[x]['BirthdayMinusTwo']) or (GameDay == playerList[x]['BirthdayPlusTwo']) or
                    (GameDay == playerList[x]['BirthdayPlusThree']))
                    and (playerList[x]['Team'] in game)):
                    # format date
                    GameDay = formattedDate.strftime("%m/%d/%y")
                    # Add player data to dict
                    Dict = dict({'Sport': sport, 'Player': playerList[x]['Player'], 'Position': playerList[x]['Position'], 
                                'Team': playerList[x]['Team'], 'Birthday': playerList[x]['Birthday'], 
                                'GameDay': GameDay, 'InjuryStatus': playerList[x]['InjuryStatus'],
                                'TeamLogoUrl': playerList[x]['TeamLogoUrl'], 'PlayerImgUrl': playerList[x]['PlayerImgUrl']})
                    # send to DB
                    # collection.insert_one(Dict)
                    collection.update_one({'Player': Dict['Player']}, {"$set": {'InjuryStatus': Dict['InjuryStatus']}})
                    # print(Dict)
                    
                    playsNearBirthdayList.append(Dict)

                    # print('*******Player Added To List*******', playerList[x]['Player'] + ' | ' +  
                    #     playerList[x]['Position']+ ' | ' +  playerList[x]['Team'] + ' | ' + 
                    #     playerList[x]['Birthday'] +' | ' + playerList[x]['InjuryStatus'])
        print('\n')
        print('All players updated in DB')

    # write players to bet on to csv
    with open('Scripting/json/playsNearBirthdayList_football.json', 'w', encoding='utf-8') as f:
        json.dump(playsNearBirthdayList, f, ensure_ascii=False, indent=4)

# compareBirthdayToNFLSchedule()