import requests
import datetime as dt
from csv import DictReader 
import csv
from helper import getAdjustedBirthdays
import json
import pymongo
from pymongo import MongoClient


apiString = 'http://127.0.0.1:8000/admin/sportsApp/addplayer/'

def convertLongNameToShort(team):
    if team == 'Anaheim Ducks':
        return 'ANA'
    elif team == 'Arizona Coyotes':
        return 'ARI'
    elif team == 'Boston Bruins':
        return 'BOS'
    elif team == 'Buffalo Sabres':
        return 'BUF'
    elif team == 'Calgary Flames':
        return 'CGY'
    elif team == 'Carolina Hurricanes':
        return 'CAR'
    elif team == 'Chicago Blackhawks':
        return 'CHI'
    elif team == 'Colorado Avalanche':
        return 'COL'
    elif team == 'Columbus Blue Jackets':
        return 'CBJ'
    elif team == 'Dallas Stars':
        return 'DAL'
    elif team == 'Detroit Red Wings':
        return 'DET'
    elif team == 'Edmonton Oilers':
        return 'EDM'
    elif team == 'Florida Panthers':
        return 'FLA'
    elif team == 'Los Angeles Kings':
        return 'LA'
    elif team == 'Minnesota Wild':
        return 'MIN'
    elif team == 'Montréal Canadiens':
        return 'MTL'
    elif team == 'Nashville Predators':
        return 'NSH'
    elif team == 'New Jersey Devils':
        return 'NJ'
    elif team == 'New York Islanders':
        return 'NYI'
    elif team == 'New York Rangers':
        return 'NYI'
    elif team == 'Ottawa Senators':
        return 'OTT'
    elif team == 'Philadelphia Flyers':
        return 'PHI'
    elif team == 'Pittsburgh Penguins':
        return 'PIT'
    elif team == 'San Jose Sharks':
        return 'SJ'
    elif team == 'Seattle Kraken':
        return 'SEA'
    elif team == 'St. Louis Blues':
        return 'STL'
    elif team == 'Tampa Bay Lightning':
        return 'TB'
    elif team == 'Toronto Maple Leafs':
        return 'TOR'
    elif team == 'Vancouver Canucks':
        return 'VAN'
    elif team == 'Vegas Golden Knights':
        return 'VGK'
    elif team == 'Washington Capitals':
        return 'WSH'
    elif team == 'Winnipeg Jets':
        return 'WPG'
    else:
        return 'No team Data for: ' + team

# **** NHL Schedule https://statsapi.web.nhl.com/api/v1/schedule?startDate=2022-06-15&endDate=2023-04-13

def compareBirthdayToNHLSchedule():

    # initial connection
    cluster = MongoClient("mongodb+srv://apaige161:nIEacKRy0zP2N1eI@cluster0.xgz1dnl.mongodb.net/?retryWrites=true&w=majority")
    print('Connected to DB')
    #define database and collection
    db = cluster["test"]
    collection = db["players"]

    print('reading player birthdays')

    sport = 'hockey'

    # Store all player data in a list of dictionaries
    with open("Scripting/csv/Player_hockey.csv", "r") as birthdayFile:
        playerList = [*csv.DictReader(birthdayFile)]
        

    getAdjustedBirthdays(playerList)

    # add week number to the end
    Url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=2022-06-15&endDate=2023-04-13' 

    # Read games by week from API
    req = requests.get(Url)
    statusCode = req.status_code

    if(statusCode != 200):
        print('Status Code: ', statusCode)
        quit()
    # convert data to JSON
    data = req.json()

    gamesData = []
    playsNearBirthdayList = []
    
    print('Getting schedule data...')
    # grab data
    for i in range(len(data['dates'])):
        date = data['dates'][i]['date']
        # loop over how ever many games are on that day
        for x in range(len(data['dates'][i]['games'])):
            awayTeam = convertLongNameToShort(data['dates'][i]['games'][x]['teams']['away']['team']['name'])
            homeTeam = convertLongNameToShort(data['dates'][i]['games'][x]['teams']['home']['team']['name'])
            gameData = {'date': date, 'awayTeam': awayTeam, 'homeTeam': homeTeam}
            # print(gameData)
            gamesData.append(gameData)

    # debug only
    # print(gamesData)

    
    for i in range(len(gamesData)):
        updatedDate = gamesData[i]['date'].split('-')
        formattedDate = dt.datetime(int(updatedDate[0]),int(updatedDate[1]),int(updatedDate[2]))
        # convert date to string
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

                    # collection.insert_one(Dict)
                    collection.update_one({'Player': Dict['Player']}, {"$set": {'InjuryStatus': Dict['InjuryStatus']}})
                    # print(Dict)

                    playsNearBirthdayList.append(Dict)

    print('\n')
    print('All players updated in DB')

    # write players to bet on to csv
    with open('Scripting/json/playsNearBirthdayList_hockey.json', 'w', encoding='utf-8') as f:
        json.dump(playsNearBirthdayList, f, ensure_ascii=False, indent=4)


# compareBirthdayToNHLSchedule()