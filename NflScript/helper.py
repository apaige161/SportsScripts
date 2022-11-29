import datetime as dt

def getAdjustedBirthdays (playerList):
    for i in range(len(playerList)):
        # convert each player birthday years to specified year
        updatedBirthday = playerList[i]['birthday'].split('-')
        playerList[i]['birthday'] = dt.date(int(updatedBirthday[0]),int(updatedBirthday[1]),int(updatedBirthday[2]))

        # Add extra days to be evaluated
        addDaysToDictionaryItem(playerList[i], 'birthdayMinusThree', playerList[i]['birthday'], -3)
        addDaysToDictionaryItem(playerList[i], 'birthdayMinusTwo', playerList[i]['birthday'], -2)
        addDaysToDictionaryItem(playerList[i], 'birthdayMinusOne', playerList[i]['birthday'], -1)
        addDaysToDictionaryItem(playerList[i], 'birthdayPlusOne', playerList[i]['birthday'], 1)
        addDaysToDictionaryItem(playerList[i], 'birthdayPlusTwo', playerList[i]['birthday'], 2)
        addDaysToDictionaryItem(playerList[i], 'birthdayPlusThree', playerList[i]['birthday'], 3)

        # convert back to string
        playerList[i]['birthday'] = playerList[i]['birthday'].strftime("%m/%d")

        #print for debug
        print(playerList[i])

def addDaysToDictionaryItem(List, newFieldStr, originalDate, numberOfDays):
    newDate = (originalDate + dt.timedelta(days=numberOfDays))
    List.update({ newFieldStr : newDate.strftime("%m/%d") })
