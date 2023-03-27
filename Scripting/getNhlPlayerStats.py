import json
import time
import requests



def getNhlStats():
    # Get team IDs
    teamsUrl = "https://statsapi.web.nhl.com/api/v1/teams"

    req = requests.get(teamsUrl)
    statusCode = req.status_code

    if(statusCode != 200):
        print('Status Code: ', statusCode)
        quit()

    data = req.json()

    teamsData = []

    teams = data['teams']
    for i in range(len(teams)):
        id = teams[i]['id']
        name = teams[i]['name']
        abbr = teams[i]['abbreviation']
        teamData = {'ID':id, 'name': name, 'abbr': abbr}
        teamsData.append(teamData)
    # print(teamsData)



    # Get roster
    playersId = []
    teamId = ''
        # Get all player IDs
    for i in range(len(teamsData)):
        teamId = teamsData[i]['ID']
        baseRosterUrl = "https://statsapi.web.nhl.com/api/v1/teams/"+ str(teamId) +"/roster"

        req = requests.get(baseRosterUrl)
        statusCode = req.status_code

        if(statusCode != 200):
            print('Status Code: ', statusCode)
            quit()

        data = req.json()

        for x in range(len(data['roster'])):
            id = data['roster'][x]['person']['id']
            playerName = data['roster'][x]['person']['fullName']
            playerInfo = {'ID': id, 'name': playerName}
            # print(playerInfo)
            playersId.append(playerInfo)
    # print(playersId)


    # get stats for each player
        # only players in the near birthday list
    with open("Scripting/json/playsNearBirthdayList_hockey.json", "r") as birthdayFile:
            playerList = json.load(birthdayFile)
    print('Adding player Ids to list of dictionaries...')
    playersToQuery = []

    for i in range(len(playerList)):
        playerName = playerList[i]['Player']
        #  add ID to dict
        for key in playersId:
            keyVal = key
            name = keyVal['name']
            id = keyVal['ID']
            if name == playerName:
                # print(name, id)
                playerList[i]['ID'] = id
                playersToQuery.append(playerList[i])
    print('IDs added to dictionary')
                
    with open('Scripting/json/PlayerPlusId_hockey.json', 'w', encoding='utf-8') as f:
        json.dump(playersToQuery, f, ensure_ascii=False, indent=4)

    print('Added player Ids to list of dictionaries...')


    id = ''

    print('Getting stats for '+str(len(playersToQuery))+' players...')

    for i in range(len(playersToQuery)):
        id = playersToQuery[i]['ID']
        name = playersToQuery[i]['Player']
        # print(name, id)
        season = '20222023'
        baseStatUrl = "https://statsapi.web.nhl.com/api/v1/people/"+str(id)+"/stats?stats=statsSingleSeason&season="+str(season)
        req = requests.get(baseStatUrl)
        statusCode = req.status_code

        if(statusCode != 200):
            print('Status Code: ', statusCode)
            quit()

        data = req.json()
        # print(data['stats'])
        print(name)
        print(id)
        if (len(data['stats'][0]['splits']) != 0 ):
            playersToQuery[i]['Stats'] = data['stats'][0]['splits'][0]['stat']
        else:
            print(name, id, ' Could not be evaluated')
        


    with open('Scripting/json/BirthdayPlayerPlusStats_hockey.json', 'w', encoding='utf-8') as f:
        json.dump(playersToQuery, f, ensure_ascii=False, indent=4)
    print('Stats added to Scripting/json/BirthdayPlayerPlusStats_hockey.json')

# getNhlStats()