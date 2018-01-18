# read in Full Roster, then remove private information for publishing online to use in 'lineups'

import pandas as pd

roster = pd.read_csv('/Users/Rodd/Desktop/websites/coachroddtalebi.github.io/data/roster.csv',
    header = 0,
    parse_dates = ['Birthday'])

public = roster[['Full Name','Goes By','Birthday','Side','Active']]

public = public[public['Active']=='Active']

public.to_csv('/Users/Rodd/Desktop/websites/coachroddtalebi.github.io/public_data/roster.csv')

'''
# Calculate age
from datetime import datetime
from datetime import date

def calculate_age(born):
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    if today.month - born.month <= 1:
        print "There was a birthday or will be a birthday soon...", born, age
    return age

public['Birthday'] = public['Birthday'].apply(lambda x: x.date())
public['Age'] = public['Birthday'].apply(calculate_age)
'''