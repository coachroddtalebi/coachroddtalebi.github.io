# read in attendance.csv and clean up so that each rower has a 0 or 1 for each date

from datetime import date, datetime
import pandas as pd
import os.path

# read in data to pandas df
attendance = pd.read_csv('../data/Attendance.csv',
    header = 0, #header is in first line
    parse_dates = [0],
    infer_datetime_format = True
    )
# clean Timestamp to just a Date
attendance['Timestamp'] = attendance['Timestamp'].apply(lambda x: x.date())
#conver to list of list
att = attendance.values.tolist()

#read in names from roster
roster = pd.read_csv('../data/Roster.csv',
    header = 0) #header is in first line
names = roster['Full Name'].tolist()

#check if file exists
cleaned = "../data/Attendance_Cleaned.csv"
if os.path.isfile(cleaned): #file exists
    cleanedDF = pd.read_csv(cleaned,
        header = 0) #header is in first line
    recentDate = datetime.strptime(max(list(cleanedDF)[1:]), '%Y-%m-%d').date()
else:
    cleanedDF = pd.DataFrame({
            'Name' : names})
    recentDate = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

# days we want to add
want = attendance.loc[attendance['Timestamp']>recentDate]
days = want['Timestamp'].tolist()
for day in days:
    cleanedDF[day] = 1
    if len(want['Who isn\'t here'].loc[want['Timestamp']==day].values) > 1:
        print "there are duplicate days. FIX!"
        print day
        exit()
    else:
        pass
    missing = want['Who isn\'t here'].loc[want['Timestamp']==day].values[0].split(', ')
    cleanedDF[day].loc[cleanedDF['Name'].isin(missing)] = 0

# save to file
cleanedDF.to_csv(cleaned, index=False)