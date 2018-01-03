import datetime

def datetimeToString(time):
        return time.strftime('%a, %d %m %Y %H:%M:%S')

def parseDatetime(time):
	print('parsing ' + time)
	return datetime.datetime(
		year(time),
		month(time),
		date(time),
		hour(time),
		minute(time),
		second(time)
	)

def year(time):
	return int(time[11:15])

def month(time):
	return int(time[8:10])

def date(time):
	return int(time[5:7])

def hour(time):
	return int(time[16:18])

def minute(time):
	return int(time[19:21])

def second(time):
	return int(time[22:24])

# 0         1         2         3         4
# 01234567890123456789012345678901234567890
# Fri, 20 10 2017 12:06:35 GMT 09:00
