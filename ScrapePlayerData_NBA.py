# All Teams: http://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams
# Specific Team: http://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/:team
# Scores: http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard

# TODO: scrape top 2 players at each position for each team
#   TODO: collect birthday
# TODO: write birthday to a csv file 

import csv
import requests

from format import formatBirthdayString


def writePlayerDataToCsvNBA():

    # if (targetSport == 'basketball'):
    #         sport = 'basketball/nba'
    # elif (targetSport == 'football'):
    #         sport = 'football/nfl'
    #         # http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams
    # elif(targetSport == 'baseball'):
    #         sport = 'baseball/mlb'
    # elif(targetSport == 'hockey'):
    #         sport = 'hockey/nhl'
    # else:
    #     print('Not an expected sport...')

    teamsUrl = 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams'

    req = requests.get(teamsUrl)
    statusCode = req.status_code

    if(statusCode != 200):
        print('Status Code: ', statusCode)
        quit()

    # convert data to JSON
    data = req.json()

    teamList:list = []

    for i in range(len(data['sports'][0]['leagues'][0]['teams'])):
        team = data['sports'][0]['leagues'][0]['teams'][i]['team']['abbreviation']
        teamList.append(team)

    print('TEAM LIST', teamList)

    teamBaseUrl = 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/'
    print(teamBaseUrl)

    # Get each team's player data
    playerList:list = []
    print('PLAYER LIST', playerList)

    # ex/ http://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/Atl/roster
    for team in teamList:
        req = requests.get(teamBaseUrl+team+'/roster')
        print('>>>>>>>>>>>>>>>>>>>> TEAM:', team, '<<<<<<<<<<<<<<<<<<<<<<')
        statusCode = req.status_code

        if(statusCode != 200):
            print('Status Code: ', statusCode)
            quit()
        
        # convert data to JSON
        data = req.json()
        numberOfPlayers = len(data['athletes'])

        for i in range(numberOfPlayers):

            playerName = data['athletes'][i]['fullName']
            playerPostion = data['athletes'][i]['position']['abbreviation']
            playerBirthday = data['athletes'][i]['dateOfBirth']

            # format date
            playerBirthday = formatBirthdayString(playerBirthday)

            injuries = data['athletes'][i]['injuries']
            if(len(injuries)>0):
                injuryStatus = data['athletes'][i]['injuries'][0]['status']
            else:
                injuryStatus = 'Healthy'
            # print(playerName, playerPostion, team, playerBirthday, injuryStatus)
            # store each player data into a list of dictionaries
            Dict = dict({'Player': playerName, 'Position': playerPostion, 'Team': team, 'Birthday': playerBirthday, 'InjuryStatus': injuryStatus})
            playerList.append(Dict)
    
    print(playerList)

    # write player data to csv file
    keys = playerList[0].keys()
    with open( ('Player_basketball.csv'), 'w', newline='' )as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(playerList)

writePlayerDataToCsvNBA()