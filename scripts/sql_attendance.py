### create db and save response

# MySQLdb is an interface for connecting to a MySQL database
# server from Python. It implements the Python Database API v2.0
# and is built on top of the MySQL C API.


### Download MySQLdb
# http://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python
# COULDNT GET IT TO WORK
# USING sqlite3 instead


import sqlite3 as lite
from datetime import date, datetime
import pandas as pd

# read in data to pandas df
attendance = pd.read_csv('Attendance.csv',
	header = 0, #header is in first line
	parse_dates = [0],
	infer_datetime_format = True
	)


# clean Timestamp to just a Date
attendance['Timestamp'] = attendance['Timestamp'].apply(lambda x: x.date())

#conver to list of list
att = attendance.values.tolist()

# DATABASE STUF
conn = lite.connect('RowData.db', #will create db if not there
		detect_types=lite.PARSE_DECLTYPES|lite.PARSE_COLNAMES) #this stuff should keep date as date not unicode
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Attendance(Date DATE, Name TEXT)")
#check if empty
c.execute("SELECT * FROM Attendance")
if c.fetchone() == None: #empty
	c.executemany("INSERT INTO Attendance VALUES(?,?)", att)
else:
	#get max date
	c.execute("SELECT Max(Date) FROM Attendance")
	recentDate = str(c.fetchone()[0])
	recentDate = datetime.strptime(recentDate, '%Y-%m-%d').date()
	trimmed = attendance.loc[attendance['Timestamp']>recentDate]
	trimmed = trimmed.values.tolist()
	c.executemany("INSERT INTO Attendance VALUES(?,?)", trimmed)

conn.commit() #commit changes
conn.close()



#### but what to do with data?
# have a list of ppl not here
# maybe import full roster and give 0,1 for attendance
# then db will be [data, name, 0/1]

# get roster names
# import csv
# with open('Roster.csv', 'rb') as f:
# 	reader = csv.reader(f)
# 	roster = list(reader)

roster = pd.read_csv('Roster.csv',
	header = 0) #header is in first line
names = roster['Full Name'].tolist()

def score(attDF, names):
	scoreDF = pd.DataFrame({
		'Date' : [],
		'Name' : [],
		'Score' : []
		})
	days = attDF['Timestamp'].tolist()
	for day in days:
		dayList = [day]*len(names)
		tempDF = pd.DataFrame({
			'Date' : dayList,
			'Name' : names,
			'Score' : [1] * len(names)
			})
		#now fill with 0s
		missing = attDF['Who isn\'t here'].loc[attDF['Timestamp']==day].values[0].split(', ')
		tempDF['Score'].loc[tempDF['Name'].isin(missing)] = 0 #will give warning. eff it

		#now append to scoreDF
		scoreDF = scoreDF.append(tempDF)

