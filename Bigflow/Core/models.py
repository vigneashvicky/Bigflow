import datetime

def convertDate(stringDate):
    return datetime.datetime.strptime(stringDate, "%d/%m/%Y").strftime("%Y-%m-%d")

def convertdbDate(stringDate):
    return datetime.datetime.strptime(stringDate, "%d-%b-%Y").strftime("%Y-%m-%d")

def convertDateTime(stringDate):
    return datetime.datetime.strptime(stringDate, "%d/%m/%Y")

def outputReturn(tubledtl, index):
   temp = tubledtl[0].split(',')
   if (len(temp) > 1):
       if (index == 0):
           return int(temp[0])
       else:
           return temp[1]
   else:
       return temp[0]

def outputReturns(tubledtl, index):
    temp = tubledtl[0].split(',')
    if (len(temp) > 1):
        if (index == 0):
            return int(temp[0])

        elif(index == 2):
            return int(temp[2])
        elif(index == 3):
            return (temp[3])
        else:
            return temp[1]
    else:
        return temp[0]

def serverip():
    return "https://174.138.120.196/bigflowdemo"

def localip():
    return "http://127.0.0.1:8000"

def token():
    return "Token 7111797114100105971106449505132"