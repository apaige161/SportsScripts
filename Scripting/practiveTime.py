import datetime

date = 1675814400
# date = 1523443804.214

convertedDateTime = datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y')

print(convertedDateTime)