import requests
import datetime as dt
from csv import DictReader 
import csv
from helper import getAdjustedBirthdays
import json
import pymongo
from pymongo import MongoClient

def compareBirthdayToMLBSchedule():
    # initial connection
    cluster = MongoClient("mongodb+srv://apaige161:nIEacKRy0zP2N1eI@cluster0.xgz1dnl.mongodb.net/?retryWrites=true&w=majority")
    print('Connected to DB')
    #define database and collection
    db = cluster["test"]
    collection = db["players"]

    print('reading player birthdays')

    sport = 'baseball'

    # Store all player data in a list of dictionaries
    with open("Scripting/csv/Player_baseball.csv", "r") as birthdayFile:
        playerList = [*csv.DictReader(birthdayFile)]
        

    getAdjustedBirthdays(playerList)

    # add week number to the end
    Url = 'http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?seasontype=2' 

    # Read games by week from API
    req = requests.get(Url)
    statusCode = req.status_code

    if(statusCode != 200):
        print('Status Code: ', statusCode)
        quit()
    # convert data to JSON
    data = req.json()

    gamesData = []
    playsNearBirthdayList:list = []
    
    print('Getting schedule data...')
    # grab game date in outer loop

    for i in range(len(data['events'])):
        shortName = data['events'][i]['shortName']
        teamArr = shortName.split('@')
        homeTeam = teamArr[1].strip()
        awayTeam = teamArr[0].strip()
        # print(awayTeam, homeTeam)

        date = data['events'][i]['date']
        updatedDate = date.split('T')
        splitDate = updatedDate[0].split('-')
        formattedDate = dt.datetime(int(splitDate[0]),int(splitDate[1]),int(splitDate[2]))
        GameDay = formattedDate.strftime("%m/%d")

        gameData = {'date': GameDay, 'awayTeam': awayTeam, 'homeTeam': homeTeam}
        print(gameData)
        gamesData.append(gameData)
    
        #   check if any player birthdays are on this day
        for x in range(len(playerList)):

            # print player if they play on their birthday
            if ( 
                ((GameDay == playerList[x]['Birthday']) or (GameDay == playerList[x]['BirthdayMinusOne']) or 
                (GameDay == playerList[x]['BirthdayMinusTwo']) or (GameDay == playerList[x]['BirthdayPlusTwo']) or
                (GameDay == playerList[x]['BirthdayPlusThree']))
                and 
                (playerList[x]['Team'] in (gamesData[i]['homeTeam'] or gamesData[i]['awayTeam']))):
                    print('*****************************************', playerList[x]['Player'] + ' | ' +  
                        playerList[x]['Position']+ ' | ' +  playerList[x]['Team'] + ' | ' + playerList[x]['Birthday'])

                    GameDay = formattedDate.strftime("%m/%d/%y")
                    
                    Dict = dict({'Sport': sport, 'Player': playerList[x]['Player'], 'Position': playerList[x]['Position'], 
                                'Team': playerList[x]['Team'], 'Birthday': playerList[x]['Birthday'], 
                                'GameDay': GameDay, 'InjuryStatus': playerList[x]['InjuryStatus'],
                                'TeamLogoUrl': playerList[x]['TeamLogoUrl'], 'PlayerImgUrl': playerList[x]['PlayerImgUrl'],
                                'Stats': {'data':-1}, 'TeamInjuryReport': [-1], '_id': i})

                    playsNearBirthdayList.append(Dict)
                    # send to DB
                    collection.insert_one(Dict) # <-- run this at start of the season
                    # collection.update_one({'Player': Dict['Player']}, {"$set": {'InjuryStatus': Dict['InjuryStatus']}})
                    print(Dict)
                    
                    

    print('\n')
    print('All players added to Scripting/json/playsNearBirthdayList_baseball.json')

    # write players to bet on to csv
    with open('Scripting/json/playsNearBirthdayList_baseball.json', 'w', encoding='utf-8') as f:
        json.dump(playsNearBirthdayList, f, ensure_ascii=False, indent=4)


# compareBirthdayToMLBSchedule()