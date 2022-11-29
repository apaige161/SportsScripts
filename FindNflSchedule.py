import requests
# from datetime import datetime
import datetime as dt
from csv import DictReader 
import csv
import json

from helper import convertBirthdayDateTimeToString, convertListBirthdayToDateTimeAndSetYear, getAdjustedBirthdays

# TODO: fix out of range error - use replace to swap 2022 with 2023?
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
today = dt.datetime.today()
year = today.year
nextYear = dt.datetime.today().year +1

getAdjustedBirthdays(playerList, year)

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
        Gamedate = WeeklyList[gameWeek]['date'].split("T")
        Gamedate = Gamedate[0]
        updatedDate = Gamedate.split('-')

        formattedDate = dt.datetime(int(updatedDate[0]),int(updatedDate[1]),int(updatedDate[2]))
        formattedDatePlus = dt.datetime((int(updatedDate[0])+1),int(updatedDate[1]),int(updatedDate[2]))

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

    print('\n')








