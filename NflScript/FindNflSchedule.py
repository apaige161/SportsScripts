import requests
import datetime as dt
from csv import DictReader 
import csv
from helper import getAdjustedBirthdays


# TODO: write my own script to grab player data from espn website - not all players in NFL list are starters, may be missing some. Add defensive players


# read NFL player CSV and load it into a dict
    # https://blog.finxter.com/convert-csv-to-dictionary-in-python/
print('reading player birthdays')

# Store all player data in a list of dictionaries
with open("/NflScript/NFLBirthdays.csv", "r") as birthdayFile:
    playerList = [*csv.DictReader(birthdayFile)]
    

getAdjustedBirthdays(playerList)

# add week number to the end
baserUrl = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week=' 
# Get data for each week
for i in range(18):
    week = i + 1
    print('***Week', week, '***')

    # Read games by week from API
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
        Gamedate = WeeklyList[gameWeek]['date'].split("T")
        Gamedate = Gamedate[0]
        updatedDate = Gamedate.split('-')
        formattedDate = dt.datetime(int(updatedDate[0]),int(updatedDate[1]),int(updatedDate[2]))
        # convert date to string
        GameDay = formattedDate.strftime("%m/%d")
        print(game + ' | Date: ' + GameDay)
        
        # check if any player birthdays are on this day
        for i in range(len(playerList)):

            # print player if they play on their birthday
            if ( 
                ((GameDay == playerList[i]['birthday']) or (GameDay == playerList[i]['birthdayMinusOne']) or 
                (GameDay == playerList[i]['birthdayMinusTwo']) or (GameDay == playerList[i]['birthdayMinusThree']) or
                (GameDay == playerList[i]['birthdayPlusOne']) or (GameDay == playerList[i]['birthdayPlusTwo']) or
                (GameDay == playerList[i]['birthdayPlusThree']))
                and 
                (playerList[i]['team'] in WeeklyList[gameWeek]['shortName'])):
                    print('*****************************************', playerList[i]['player'] + ' | ' +  playerList[i]['position']+ ' | ' +  playerList[i]['team'] + ' | ' + playerList[i]['birthday'])
                    # TODO: Write player data to a file
                    

    print('\n')








