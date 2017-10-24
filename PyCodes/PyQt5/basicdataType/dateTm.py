from datetime import datetime, date,timedelta,time
import re
import calendar
# import time

cal = calendar.month(2008, 1)
print ("Here is the calendar:")
print (cal)

delta = timedelta(hours=1,milliseconds=123,microseconds=123456)
print(delta.total_seconds())
resolution = timedelta(0,0,1)
print(resolution,resolution.total_seconds())

dt = datetime.now()
print(dt.utcnow())


d = date.fromordinal(730920) # 730920th day after 1. 1. 0001
print(d)

d = date(2002, 3, 11)
t = d.timetuple()
print(type(t),t)
# for i in t:  
#     print(i)  ## 
ic = d.isocalendar()
for i in ic:    
    print(i)

print(d.isoformat())
print(d.strftime("%d/%m/%y"))
print(d.strftime("%A %d. %B %Y"))
print('The {1} is {0:%d}, the {2} is {0:%B}.'.format(d, "day", "month"))

d = date(2005, 7, 14)
t = time(12, 30)
datetime.combine(d, t)
# datetime.datetime(2005, 7, 14, 12, 30)
datetime.now()   
# datetime.datetime(2007, 12, 6, 16, 29, 43, 79043)   # GMT +1
datetime.utcnow()   
# datetime.datetime(2007, 12, 6, 15, 29, 43, 79060)
# Using datetime.strptime()
dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
## 格式化 日期时间
d = datetime.now()
print('{:%Y-%m-%d %H %M %S}'.format(d))
print('{:%Y-%m-%d %H %M %S}'.format(dt))



## 1 当前时间  时间---》日期
import time
tm = time.time()
print('time:',tm)
dt = time.localtime(time.time())
print(type(dt),dt)
tmStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
print(tmStr)

dt = datetime.now()
print(type(dt),dt)
print(dt.year,dt.month,dt.day,dt.second,dt.microsecond)



# 2 日期字符串--> 日期  
s='2015-12-21 15:01:28'
timeTuple = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
print(timeTuple)
print(timeTuple.timestamp())

## 3 时间戳  日期---》时间

tm = time.gmtime(timeTuple.timestamp())
print(tm,int(time.time()))
print(time.ctime(timeTuple.timestamp()),time.ctime(time.time()))
# timestamp to time tuple in UTC
timestamp = 1226527167.595983
time_tuple = time.gmtime(timestamp)  # second
print (repr(time_tuple))



# 4 日期相加减
now = datetime.now() # datetime.datetime(2015, 12, 16, 15, 6, 37, 420000)
dayOfweek = now.isoweekday()
if dayOfweek == 1: # Monday
    last_time = now + timedelta(days=-3)
else:
    last_time = now + timedelta(hours=-1)
print(last_time)

dl = timedelta(microseconds=5000)
print('时间间隔%s'%dl)
print(date.min,date.max)
