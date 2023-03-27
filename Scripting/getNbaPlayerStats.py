import csv
import time
import json

from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players



def getNbaStats():
    ######################### Map players with IDs ###################################

    url = ''

    # Get all player IDs
    nba_players = players.get_players()
    print('Number of players fetched: {}'.format(len(nba_players)))
    mapped_nba_players = []
    # map player name to ID

    for i in range(len(nba_players)) :
        id = nba_players[i]['id']
        full_name = nba_players[i]['full_name']
        player_data = {'id': id, 'fullName': full_name}
        mapped_nba_players.append(player_data)



    ######################### Update dictionary with IDs ###################################

    # Store all player data in a list of dictionaries
    with open("Scripting/json/playsNearBirthdayList_basketball.json", "r") as birthdayFile:
        playerList = json.load(birthdayFile)

    PlayerWithId = []

    for x in range(len(playerList)):
        playerName = playerList[x]['Player']
        # Find ID for Player
        for key in mapped_nba_players:
            keyVal = key
            name = keyVal['fullName']
            id = keyVal['id']
            if name == playerName:
                # print(name, id)
                playerList[x]['ID'] = id
                PlayerWithId.append(playerList[x])

    print('IDs added to dictionary')
            
    with open('Scripting/json/PlayerPlusId.json', 'w', encoding='utf-8') as f:
                json.dump(PlayerWithId, f, ensure_ascii=False, indent=4)
        


    ######################### Update dictionary with stats (from api call) ###################################
    print(len(PlayerWithId), 'Player\'s stats are getting updated')
    for x in range(len(PlayerWithId)):
        time.sleep(0.5)
        career = playercareerstats.PlayerCareerStats(player_id=str(PlayerWithId[x]['ID']))
        Dict = career.get_dict()

        headers = Dict['resultSets'][0]['headers']
        stats = Dict['resultSets'][0]['rowSet'][(len(Dict['resultSets'][0]['rowSet']) -1)]

        statDict = {}
        
        #  map headers to stats
        for i in range(len(headers)):
            statDict[headers[i]] = stats[i]
        print('Stats added for:', PlayerWithId[x]['Player'])

        PlayerWithId[x]['Stats'] = statDict

    with open('Scripting/json/BirthdayPlayerPlusStats_basketball.json', 'w', encoding='utf-8') as f:
        json.dump(PlayerWithId, f, ensure_ascii=False, indent=4)
    print('Added JSON to Scripting/json/BirthdayPlayerPlusStats.json')
