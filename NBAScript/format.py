import datetime as dt

def formatBirthdayString(dateString):
    date = dateString.split('T')
    preFormattedDate = date[0].split('-')
    formattedDateTime = dt.date(int(preFormattedDate[0]),int(preFormattedDate[1]), int(preFormattedDate[2]))
    return formattedDateTime.strftime("%m/%d/%y")