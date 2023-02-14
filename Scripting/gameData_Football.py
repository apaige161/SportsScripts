import requests
from csv import DictReader 
import json
import datetime as dt

def getFootballGameData():

    # add week number to the end
    Url = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week=' 
    gamesData = []

    for i in range(18):
        week = i + 1
        print('***Week', week, '***')

        # Read games by week from API
        adjustedUrl = Url + str(week)
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
            GameDay = formattedDate.strftime("%m/%d/%y")

            GameArr = game.split(' ')
            awayTeam = GameArr[0]
            GameArr = game.split(' ')
            homeTeam = GameArr[2]

            print('Home:', homeTeam)
            print('Away:', awayTeam)
            gameData = {'date': GameDay, 'awayTeam': awayTeam, 'homeTeam': homeTeam}

            gamesData.append(gameData)


    # write players to bet on to csv
    with open('Scripting/json/gameData_football.json', 'w', encoding='utf-8') as f:
        json.dump(gamesData, f, ensure_ascii=False, indent=4)

getFootballGameData()