import requests
import datetime as dt
from csv import DictReader 
import csv
from helper import getAdjustedBirthdays
import json
import pymongo
from pymongo import MongoClient

def compareBirthdayToNBASchedule():
    # initial connection
    cluster = MongoClient("mongodb+srv://apaige161:nIEacKRy0zP2N1eI@cluster0.xgz1dnl.mongodb.net/?retryWrites=true&w=majority")
    print('Connected to DB')
    #define database and collection
    db = cluster["test"]
    collection = db["players"]

    print('reading player birthdays')

    sport = 'basketball'

    # Store all player data in a list of dictionaries
    with open("Scripting/csv/Player_basketball.csv", "r") as birthdayFile:
        playerList = [*csv.DictReader(birthdayFile)]
        

    getAdjustedBirthdays(playerList)

    # add week number to the end
    Url = 'https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json' 

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
    for i in range(len(data['leagueSchedule']['gameDates'])):
        date = data['leagueSchedule']['gameDates'][i]['gameDate']
        # print(date)
        # loop over how ever many games are on that day
        for x in range(len(data['leagueSchedule']['gameDates'][i]['games'])):
            awayTeam = data['leagueSchedule']['gameDates'][i]['games'][x]['awayTeam']['teamTricode']
            homeTeam = data['leagueSchedule']['gameDates'][i]['games'][x]['homeTeam']['teamTricode']
            gameData = {'date': date, 'awayTeam': awayTeam, 'homeTeam': homeTeam}
            # print(gameData)
            gamesData.append(gameData)

    # debug only
    # print(gamesData)

    
    for i in range(len(gamesData)):
        updatedDate = gamesData[i]['date'].split(' ')
        # convert date to string
        splitDate = updatedDate[0].split('/')
        formattedDate = dt.datetime(int(splitDate[2]),int(splitDate[0]),int(splitDate[1]))
        GameDay = formattedDate.strftime("%m/%d")
        print('Date: ' + GameDay + ' | ' + gamesData[i]['awayTeam'] + ' @ ' + gamesData[i]['homeTeam'])
        
        # check if any player birthdays are on this day
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
                                'TeamLogoUrl': playerList[x]['TeamLogoUrl'], 'PlayerImgUrl': playerList[x]['PlayerImgUrl']})

                    # send to DB
                    # collection.insert_one(Dict) <-- run this at start of the season
                    collection.update_one({'Player': Dict['Player']}, {"$set": {'InjuryStatus': Dict['InjuryStatus']}})
                    # print(Dict)
                    
                    playsNearBirthdayList.append(Dict)
    # print(playsNearBirthdayList)

    print('\n')
    print('All players updated in DB')

    # write players to bet on to csv
    with open('Scripting/json/playsNearBirthdayList_basketball.json', 'w', encoding='utf-8') as f:
        json.dump(playsNearBirthdayList, f, ensure_ascii=False, indent=4)


# compareBirthdayToNBASchedule()