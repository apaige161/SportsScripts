import requests
from csv import DictReader 
import json

def getBasketballGameData():

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
    
    print('Getting schedule data...')
    # grab game date in outer loop
    for i in range(len(data['leagueSchedule']['gameDates'])):
        date = data['leagueSchedule']['gameDates'][i]['gameDate']
        dateArr = date.split(' ')
        date = dateArr[0]
        print(date)

        # loop over how ever many games are on that day
        for x in range(len(data['leagueSchedule']['gameDates'][i]['games'])):
            awayTeam = data['leagueSchedule']['gameDates'][i]['games'][x]['awayTeam']['teamTricode']
            homeTeam = data['leagueSchedule']['gameDates'][i]['games'][x]['homeTeam']['teamTricode']
            gameData = {'date': date, 'awayTeam': awayTeam, 'homeTeam': homeTeam}
            # print(gameData)
            gamesData.append(gameData)

    # write players to bet on to csv
    with open('Scripting/json/gameData_basketball.json', 'w', encoding='utf-8') as f:
        json.dump(gamesData, f, ensure_ascii=False, indent=4)

getBasketballGameData()