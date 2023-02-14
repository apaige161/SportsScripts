import requests
from csv import DictReader 
import json

from FindSchedule_NHL import convertLongNameToShort

def getHockeyGameData():

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
    
    print('Getting schedule data...')
    # grab data
    for i in range(len(data['dates'])):
        date = data['dates'][i]['date']
        dateArr = date.split('-')
        formattedDate = dateArr[1] + '/' + dateArr[2] + '/' + dateArr[0]
        # loop over how ever many games are on that day
        for x in range(len(data['dates'][i]['games'])):
            awayTeam = convertLongNameToShort(data['dates'][i]['games'][x]['teams']['away']['team']['name'])
            homeTeam = convertLongNameToShort(data['dates'][i]['games'][x]['teams']['home']['team']['name'])
            gameData = {'date': formattedDate, 'awayTeam': awayTeam, 'homeTeam': homeTeam}
            # print(gameData)
            gamesData.append(gameData)

    # write players to bet on to csv
    with open('Scripting/json/gameData_hockey.json', 'w', encoding='utf-8') as f:
        json.dump(gamesData, f, ensure_ascii=False, indent=4)

getHockeyGameData()