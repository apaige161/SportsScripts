import requests
# from datetime import datetime
import datetime
from csv import DictReader 
import csv
import json

# TODO: refactor how multi year seasons are handled
# TODO: add logic to check if a player plays +/- 1 day (maybe several days?) from birthday
# TODO: write my own script to grab player data from espn website - not all players in NFL list are starters, may be missing some. Add defensive players

# read NFL player CSV and load it into a dict
    # https://blog.finxter.com/convert-csv-to-dictionary-in-python/
print('reading player birthdays')

# Store all player data in a list of dictionaries
with open("NFLBirthdays.csv", "r") as birthdayFile:
    playerList = [*csv.DictReader(birthdayFile)]
    
# Get todays year
today = datetime.date.today()
year = today.year

for i in range(len(playerList)):
    # convert all birthday years to current year
    updatedBirthday = playerList[i]['birthday'].split('-')
    updatedBirthday[0] = str(year)
    playerList[i]['birthday'] = updatedBirthday[0] + '-' + updatedBirthday[1] + '-' + updatedBirthday[2]
    # print the list for debug
    # print(playerList[i]['player'] + ' | ' +  playerList[i]['birthday'] + ' | ' +  playerList[i]['position']+ ' | ' +  playerList[i]['team'])


baserUrl = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week=' # add week number to the end
# Get data for each week
for i in range(18):
    week = i + 1
    print('***Week', week, '***')

    # Read week 1 games from API
    adjustedUrl = baserUrl + str(week)
    req = requests.get(adjustedUrl)
    statusCode = req.status_code

    # convert data to JSON
    data = req.json()

    if(statusCode != 200):
        print('Status Code: ', statusCode)
        quit()

    WeeklyList = data['events']

    for gameWeek in range(len(WeeklyList)):
        game = WeeklyList[gameWeek]['shortName']
        date = WeeklyList[gameWeek]['date'].split("T")
        date = date[0]

        print('Game #'+ str(gameWeek + 1) + ' | '+ game + ' | Date: ' + date)

        # check if any player birthdays are on this day
        for i in range(len(playerList)):

            # print player if they play on thier birthday
            if (date == playerList[i]['birthday'] and (playerList[i]['team'] in WeeklyList[gameWeek]['shortName'])):
                print('*****************************************', playerList[i]['player'] + ' | ' +  playerList[i]['position']+ ' | ' +  playerList[i]['team'] + ' | ' + playerList[i]['birthday'])

            # handle multi year seasons
            if ( str((year + 1)) in date):
                newYearPlayer = playerList[i]['birthday'].split('-')
                newYearPlayer[0] = str((year + 1))
                newYearDate = date.split('-')
                newYearDate[0] = str((year + 1))
                if (newYearDate == newYearPlayer) and (playerList[i]['team'] in WeeklyList[gameWeek]['shortName']):
                    print('*****************************************', playerList[i]['player'] + ' | ' +  playerList[i]['position']+ ' | ' +  playerList[i]['team'] + ' | ' + playerList[i]['birthday'])
        
    print('\n')






# write JSON to a new file
# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)



# wjdata = requests.get('url').json()
# print wjdata['data']['current_condition'][0]['temp_C']


