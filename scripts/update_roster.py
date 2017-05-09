# after downloading all files from GoogleSheets
# and after clean_attendance.py has been run
# update the roster.csv with new data


from datetime import date, datetime, timedelta
import pandas as pd
import os.path

# load in roster
roster = pd.read_csv('../data/Roster.csv',
    header = 0)
names = roster['Full Name'].tolist()
roster['Attendance Score'] = 0

# note the date the csv is most recently updated on
roster['Last Updated'] = str(datetime.now())

# update attendance
#note that attendance.csv pull and attendance_clean must have already been done
attendance = pd.read_csv('../data/Attendance_Cleaned.csv',header = 0)
for name in names:
    score = attendance.mean(axis=1).loc[attendance['Name']==name].values[0]
    roster['Attendance Score'].loc[roster['Full Name']==name] = int(score*100)

# update absent
absent = pd.read_csv('../data/Absence.csv',
                     header = 0, #header is in first line
                     parse_dates = [0,2,3],
                     infer_datetime_format = True)
# clean Timestamp to just a Date
absent['Timestamp'] = absent['Timestamp'].apply(lambda x: x.date())
absent['Start Date'] = absent['Start Date'].apply(lambda x: x.date())
absent['Last Date'] = absent['Last Date'].apply(lambda x: x.date())

tomorrow = date.today() + timedelta(days=1)
# filter to see who will be absent tomorrow and mark them as such
absentPpl = absent['Name'].loc[absent['Start Date'] <= tomorrow].loc[absent['Last Date'] >= tomorrow].values
for name in absentPpl:
    roster['Status'].loc[roster['Full Name']==name] = 'Absent'

# update injured
injured = pd.read_csv('../data/Injury_Report.csv',
                     header = 0, #header is in first line
                     parse_dates = [0],
                     infer_datetime_format = True)
# clean Timestamp to just a Date
injured['Timestamp'] = injured['Timestamp'].apply(lambda x: x.date())

# filter to see who will be absent tomorrow and mark them as such
injured['Last Date'] = injured.apply(lambda x: x['Timestamp'] + timedelta(days=int(x['(Additional) Days off required'])), axis=1)

injuredPpl = injured['Name'].loc[injured['Last Date'] >= tomorrow].values
for name in injuredPpl:
    roster['Status'].loc[roster['Full Name']==name] = 'Injured'

# save updated roster
roster.to_csv('../data/Roster.csv', index=False)