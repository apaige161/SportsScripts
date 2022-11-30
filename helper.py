import datetime as dt

def getAdjustedBirthdays (playerList):
    for i in range(len(playerList)):
        # convert each player birthday years to specified year
        updatedBirthday = playerList[i]['Birthday'].split('/')

        # print(updatedBirthday)
        # playerList[i]['Birthday'] = dt.date(int(updatedBirthday[0]),int(updatedBirthday[1]),int(updatedBirthday[2])) ->y,m,d
        playerList[i]['Birthday'] = dt.date(int(updatedBirthday[0]),int(updatedBirthday[1]),int(updatedBirthday[2]))

        # Add extra days to be evaluated
        addDaysToDictionaryItem(playerList[i], 'BirthdayMinusThree', playerList[i]['Birthday'], -3)
        addDaysToDictionaryItem(playerList[i], 'BirthdayMinusTwo', playerList[i]['Birthday'], -2)
        addDaysToDictionaryItem(playerList[i], 'BirthdayMinusOne', playerList[i]['Birthday'], -1)
        addDaysToDictionaryItem(playerList[i], 'BirthdayPlusOne', playerList[i]['Birthday'], 1)
        addDaysToDictionaryItem(playerList[i], 'BirthdayPlusTwo', playerList[i]['Birthday'], 2)
        addDaysToDictionaryItem(playerList[i], 'BirthdayPlusThree', playerList[i]['Birthday'], 3)

        # convert back to string
        playerList[i]['Birthday'] = playerList[i]['Birthday'].strftime("%m/%d")

        #print for debug
        # print(playerList[i])

def addDaysToDictionaryItem(List, newFieldStr, originalDate, numberOfDays):
    newDate = (originalDate + dt.timedelta(days=numberOfDays))
    List.update({ newFieldStr : newDate.strftime("%m/%d") })
