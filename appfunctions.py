
def convertGivenTimeToEpoch(year, month, day, hour, minute, ampm):
    from datetime import *
    m2 = str(hour) + ":" + str(minute) + " " + str(ampm.lower())
    m2 = datetime.strptime(m2, '%I:%M %p')
    m2 = str(m2)
    m2 = m2.split(" ")[1]
    m2.split(":")

    time2 = datetime.datetime(1970,1,1,0,0,0)
    time1 = datetime.datetime(year, month, day, m2[0], m2[1], m2[2])
    x = (time1 - time2).total_seconds()
    return x
