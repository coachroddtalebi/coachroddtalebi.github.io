# input:
# $python update_erg.py "2k"

import sys
from datetime import date, datetime
import pandas as pd
import os.path

if len(sys.argv) > 1:
    ergtest = sys.argv[1]
else:
    print "You didn't mention which test to update"
    exit()

filename = '../data/' + ergest + '.csv'
scores = pd.read_csv(filename,
    header = 0, #header is in first line
    parse_dates = [0],
    infer_datetime_format = True
    )
# clean Timestamp to just a Date
scores['Timestamp'] = scores['Timestamp'].apply(lambda x: x.date())

#sort by timestamp
scores = scores.sort(['Timestamp'], ascending = True)

#read in names from roster
roster = pd.read_csv('../data/Roster.csv',
    header = 0) #header is in first line
names = roster['Full Name'].tolist()

if ergtest == "2k":
	# Timestamp, Name, 500m, 1000m, 1500m, 2000m, AveSplit, Time, Watts
	
	for name in names:
		#get PR and most recent (time or average?)
		if len(scores['Time'].loc[scores['Name']==name].values)>=1:
			roster['2kTimePR'].loc[roster['Full Name']==name] = max(scores['Time'].loc[scores['Name']==name].values)
			roster['2kSplitPR'].loc[roster['Full Name']==name] = max(scores['AveSplit'].loc[scores['Name']==name].values)
			roster['2kWattsPR'].loc[roster['Full Name']==name] = max(scores['Watts'].loc[scores['Name']==name].values)

			# scores are sorted by time so the last row instance will work
			roster['2kTimeRecent'].loc[roster['Full Name']==name] = scores['Time'].loc[scores['Name']==name].values[-1]
			roster['2kSplitRecent'].loc[roster['Full Name']==name] = scores['AveSplit'].loc[scores['Name']==name].values[-1]
		else:
			print "no scores to report for", name

elif ergtest == "6k":
	# Timestamp, Name, 1000m, 2000m, 3000m, 4000m, 5000m, 6000m, AveSplit, Time, Watts
	
	for name in names:
		#get PR and most recent (time or average?)
		if len(scores['Time'].loc[scores['Name']==name].values)>=1:
			roster['6kTimePR'].loc[roster['Full Name']==name] = max(scores['Time'].loc[scores['Name']==name].values)
			roster['6kSplitPR'].loc[roster['Full Name']==name] = max(scores['AveSplit'].loc[scores['Name']==name].values)
			roster['6kWattsPR'].loc[roster['Full Name']==name] = max(scores['Watts'].loc[scores['Name']==name].values)

			# scores are sorted by time so the last row instance will work
			roster['6kTimeRecent'].loc[roster['Full Name']==name] = scores['Time'].loc[scores['Name']==name].values[-1]
			roster['6kSplitRecent'].loc[roster['Full Name']==name] = scores['AveSplit'].loc[scores['Name']==name].values[-1]
		else:
			print "no scores to report for", name

elif ergtest == "30min":
	# Timestamp, Name, 10min, 20min, 30min, AveSplit, Meters
	
	for name in names:
		#get PR and most recent (time or average?)
		if len(scores['Meters'].loc[scores['Name']==name].values)>=1:
			roster['30mMetersPR'].loc[roster['Full Name']==name] = max(scores['Meters'].loc[scores['Name']==name].values)
			roster['30mSplitPR'].loc[roster['Full Name']==name] = max(scores['AveSplit'].loc[scores['Name']==name].values)

			# scores are sorted by time so the last row instance will work
			roster['30mMetersRecent'].loc[roster['Full Name']==name] = scores['Meters'].loc[scores['Name']==name].values[-1]
			roster['30mSplitRecent'].loc[roster['Full Name']==name] = scores['AveSplit'].loc[scores['Name']==name].values[-1]
		else:
			print "no scores to report for", name

else:
	print "I don't recognize that erg test. Try again"
	exit()

# save to file
roster.to_csv('../data/Roster.csv', index=False)