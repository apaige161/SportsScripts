
import json
from pymongo import MongoClient


def setplayerStatsPlusTeamInjuries(sport):
    ############# DB setup
    cluster = MongoClient("mongodb+srv://apaige161:nIEacKRy0zP2N1eI@cluster0.xgz1dnl.mongodb.net/?retryWrites=true&w=majority")
    print('Connected to DB')
    #define database and collection
    db = cluster["test"]
    collection = db["players"]

    ############# Read player injury Data

    injuredPlayerFilePath = 'Scripting/json/injuryReport_'+sport+'.json'
    birthdayPlayerPlusStats = 'Scripting/json/BirthdayPlayerPlusStats_'+sport+'.json'

    # read JSOJN files
    with open(injuredPlayerFilePath, encoding='utf-8') as birthdayFile:
        injuredPlayerList = json.load(birthdayFile)

    with open(birthdayPlayerPlusStats, encoding='utf-8') as birthdayFile:
        birthdayPlayerList = json.load(birthdayFile)

    teamInjuryReport = []
    # Add team mate's name to injured list
    for i in range(len(birthdayPlayerList)):
        #  player to search for teammates
        team = birthdayPlayerList[i]['Team']
        name = birthdayPlayerList[i]['Player']
        # print(name, team)
        teamInjuryReport = []
        # loop over injury report 
        for x in range(len(injuredPlayerList)):
            InjuredplayerTeam = injuredPlayerList[x]['Team']
            InjuredPlayerName = injuredPlayerList[x]['Player']
            InjuredPlayerPosition = injuredPlayerList[x]['Position']
            InjuredPlayerStatus = injuredPlayerList[x]['InjuryStatus']
            if InjuredplayerTeam == team:
                # print('Injured teammate: ', InjuredPlayerName, InjuredplayerTeam)
                if InjuredPlayerName != name:
                    teamInjuryReport += [InjuredPlayerName + ' - ' + InjuredPlayerPosition + ' - ' + InjuredPlayerStatus]
                birthdayPlayerList[i]['TeamInjuryReport'] = teamInjuryReport

        # collection.update_one(
    #     {'Player': birthdayPlayerList[i]['Player']}, 
    #     {"$set": 
    #         {
    #             'Stats': birthdayPlayerList[i]['Stats'], 'InjuryStatus': birthdayPlayerList[i]['TeamInjuryReport']
    #         }
    #     })
        # collection.insert_one(birthdayPlayerList[i])
        # print(name, 'Added to DB')

            
    with open('Scripting/json/BirthdayPlayerPlusStatsAndInjury_'+sport+'.json', 'w', encoding='utf-8') as f:
        json.dump(birthdayPlayerList, f, ensure_ascii=False, indent=4)
    print('Added JSON to BirthdayPlayerPlusStatsAndInjury_'+sport+'.json')


    
setplayerStatsPlusTeamInjuries('basketball')
setplayerStatsPlusTeamInjuries('hockey')