# read in Full Roster, then remove private information for publishing online to use in 'lineups'

import pandas as pd

roster = pd.read_csv('/Users/Rodd/Desktop/websites/coachroddtalebi.github.io/data/roster.csv',
    header = 0)

public = roster[['Full Name','Goes By','Side','Active']]

public = public[public['Active']=='Active']

public.to_csv('/Users/Rodd/Desktop/websites/coachroddtalebi.github.io/public_data/roster.csv')