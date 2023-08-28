
from ScrapePlayerData_NBA import writePlayerDataToCsvNBA
from ScrapePlayerData_NFL import writePlayerDataToCsvNFL
from ScrapePlayerData_NHL import writePlayerDataToCsvNHL
from ScrapePlayerData_MLB import writePlayerDataToCsvMLB

from FindSchedule_NHL import compareBirthdayToNHLSchedule
from FindSchedule_NFL import compareBirthdayToNFLSchedule
from FindSchedule_NBA import compareBirthdayToNBASchedule

from FindSchedule_MLB import compareBirthdayToMLBSchedule

from WritePlayersToDb import writePlayersToDb

from setInjuredTeamdataToPlayerData import setplayerStatsPlusTeamInjuries

from getNhlPlayerStats import getNhlStats
from getNbaPlayerStats import getNbaStats

from injuryReport import getInjuryReport



########################################## collect player data
# writePlayerDataToCsvNBA()
writePlayerDataToCsvNFL() # good to go
# writePlayerDataToCsvNHL()
# writePlayerDataToCsvMLB()

######################################### compare schedule to player birthday
# compareBirthdayToNHLSchedule()
compareBirthdayToNFLSchedule() # good to go
# compareBirthdayToNBASchedule()
# compareBirthdayToMLBSchedule()

######################################### Get injury report
# getInjuryReport("basketball")
getInjuryReport("football")
# getInjuryReport("hockey")

######################################## Add Stats
# getNbaStats()
# getNhlStats()
# writeNbaStatsToDb()
# writeNhlStatsToDb()

######################################## Add Injury report to player data
# setplayerStatsPlusTeamInjuries('basketball')
# setplayerStatsPlusTeamInjuries('hockey')

setplayerStatsPlusTeamInjuries('football')

# writePlayersToDb('basketball')
# writePlayersToDb('hockey')

writePlayersToDb('football')