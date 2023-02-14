import requests
from csv import DictReader 
import datetime
import json

# api from https://www.thelines.com/odds/

def getOdds():

    BaseUrl = 'https://metabet.static.api.areyouwatchingthis.com/api/odds.json?apiKey=219f64094f67ed781035f5f7a08840fc&location=NJ&leagueCode='
    nba = 'BKP'
    nhl = 'HKN'
    mls = 'SOM'
    nfl = 'FBP'
    mlb = 'BBM'

    sportsArr = [nba,nhl,mls,nfl,mlb]

    for sport in sportsArr:




        # Read games by week from API
        req = requests.get(BaseUrl+sport)
        statusCode = req.status_code

        if(statusCode != 200):
            print('Status Code: ', statusCode)
            quit()
        # convert data to JSON
        data = req.json()

        gamesData = []

        resultList = data['results']


        for i in range(len(resultList)):
            # print(resultList[i])
            date = resultList[i]['date']
            # date is not in the right format, remove the last three digits
            dateStr = str(date)[:-3]
            convertedDateTime = datetime.datetime.utcfromtimestamp(int(dateStr)).strftime('%d-%m-%Y')

            sport = resultList[i]['sport']
            team1 = resultList[i]['team1Initials']
            team2 = resultList[i]['team2Initials']
            odds = resultList[i]['odds']

            # oddsOverUnder = odds['overUnder']

            gameData = {'date': convertedDateTime, 'sport': sport, 'team1': team1, 'team2': team2, 'odds': odds}
            # print(gameData, "\n")
            gamesData.append(gameData)
        

        # write players to bet on to csv
        with open('Scripting/json/Odds/'+sport+'_Team_odds.json', 'w', encoding='utf-8') as f:
            json.dump(gamesData, f, ensure_ascii=False, indent=4)

getOdds()