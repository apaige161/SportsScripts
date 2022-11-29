import datetime as dt

def getAdjustedBirthdays (playerList, year):
    for i in range(len(playerList)):
        # convert each player birthday years to specified year
        convertListBirthdayToDateTimeAndSetYear(playerList, i, year)

        # Add extra days to be evaluated
        addDaysToDictionaryItem(playerList[i], 'birthdayMinusThree', playerList[i]['birthday'], -3)
        addDaysToDictionaryItem(playerList[i], 'birthdayMinusTwo', playerList[i]['birthday'], -2)
        addDaysToDictionaryItem(playerList[i], 'birthdayMinusOne', playerList[i]['birthday'], -1)
        addDaysToDictionaryItem(playerList[i], 'birthdayPlusOne', playerList[i]['birthday'], 1)
        addDaysToDictionaryItem(playerList[i], 'birthdayPlusTwo', playerList[i]['birthday'], 2)
        addDaysToDictionaryItem(playerList[i], 'birthdayPlusThree', playerList[i]['birthday'], 3)

        # convert back to string
        # convertBirthdayDateTimeToString(playerList, i)
        playerList[i]['birthday'] = playerList[i]['birthday'].strftime("%m/%d")

        #print for debug
        print(playerList[i])

def addDaysToDictionaryItem(List, newFieldStr, originalDate, numberOfDays):
    newDate = (originalDate + dt.timedelta(days=numberOfDays))
    List.update({ newFieldStr : newDate.strftime("%m/%d") })

def convertListBirthdayToDateTimeAndSetYear(List,index,year):
    # convert all birthday years to specified year
    updatedBirthday = List[index]['birthday'].split('-')
    updatedBirthday[0] = str(year)
    # convert string to datetime
    List[index]['birthday'] = dt.date(int(updatedBirthday[0]),int(updatedBirthday[1]),int(updatedBirthday[2]))
    

def convertBirthdayDateTimeToString(List,index):
     List[index]['birthday'] = List[index]['birthday'].strftime("%m/%d/%Y")