from datetime import datetime
import pytz
def convertGivenTimeToEpoch(year, month, day, hour, minute, ampm):
    m2 = str(hour) + ":" + str(minute) + " " + str(ampm.lower())
    m2 = datetime.datetime.strptime(m2, '%I:%M %p')
    m2 = str(m2)
    m2 = m2.split(" ")[1]
    m2 = m2.split(":")
    m2[0] = m2[0].replace(":", "")
    m2[1] = m2[1].replace(":", "")
    m2[2] = m2[2].replace(":", "")
    print(m2[0] + ":" + m2[1] + ":" + m2[2])
    time = datetime.datetime(int(year), int(month), int(day), int(m2[0]), int(m2[1]), int(m2[2])).timestamp()
    return str(time)
#Usage: convertGivenTimeToEpoch("2019", "6", "26", "11", "00", "pm")

