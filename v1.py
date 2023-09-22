import time
import sqlite3
def getTime():
    localTime = time.localtime()
    day = int(time.strftime('%d',localTime))
    month = int(time.strftime('%m', localTime))
    year = int(time.strftime('%Y', localTime))

    hour = int(time.strftime('%H',localTime))
    minute = int(time.strftime('%M', localTime))
    return minute, hour, day, month, year
clockOrder = ('minute', 'hour', 'day', 'month', 'year')
con = sqlite3.connect("tutorial.db")
activities = ('bedtime', 'working', 'down time', 'flying', 'away')
print("welcome, what are you up to?")
for x in activities:
    if activities.index(x) == (len(activities)-1):
        print(f'{activities.index(x)+1}.{x}', end = ":\n")
    else:
        print(f'{activities.index(x)+1}.{x}', end = ", ")
while True:

    answer = input()
    try:
        answer = int(answer)
        if answer <= len(activities):
            answer = answer-1
            break
        else:
            print("Number is not valid, please enter a vaild number:")
    except ValueError:
        print("invalid entry, please enter a valid number:")

cur = con.cursor()
try:
    res = cur.execute("SELECT * FROM tracking")
except sqlite3.OperationalError:
    cur.execute("CREATE TABLE tracking(activity, startMinute, startHour, startDate, startMonth, startYear, endMinute, endHour, endDate, endMonth,endYear)")
    print("table created")


clock = getTime()
res = cur.execute("SELECT * FROM tracking WHERE endMinute = 0")
if len(res.fetchall()) > 0:
    data = (clock[0], clock[1], clock[2], clock[3], clock[4])
    cur.execute("UPDATE tracking SET endMinute = ?, endHour = ?, endDate = ?, endMonth = ?, endYear = ? WHERE endYear = 0", data)
data = (activities[answer], clock[0], clock[1], clock[2], clock[3], clock[4],0,0,0,0,0)
cur.execute("INSERT INTO tracking(activity, startminute, startHour, startDate, startMonth, startYear, endMinute, endHour, endDate, endMonth, endYear) VALUES(?,?,?,?,?,?,?,?,?,?,?)", data)
con.commit()
print("complete")

##cur.execute("UPDATE tracking SET endMinute = ?, endHour = ?, end WHERE endYear = 0", '100')
##con.commit()
##con.close()
##print("done")

##cur.execute("DELETE FROM tracking")
##con.commit()
