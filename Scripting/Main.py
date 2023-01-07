
from ScrapePlayerData_NBA import writePlayerDataToCsvNBA
from ScrapePlayerData_NFL import writePlayerDataToCsvNFL
from ScrapePlayerData_NHL import writePlayerDataToCsvNHL

from FindSchedule_NHL import compareBirthdayToNHLSchedule
from FindSchedule_NFL import compareBirthdayToNFLSchedule
from FindSchedule_NBA import compareBirthdayToNBASchedule



# collect player data
writePlayerDataToCsvNBA()
writePlayerDataToCsvNFL()
writePlayerDataToCsvNHL()

# compare schedule to player birthday
compareBirthdayToNHLSchedule()
compareBirthdayToNFLSchedule()
compareBirthdayToNBASchedule()