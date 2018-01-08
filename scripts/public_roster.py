# read in Full Roster, then remove private information for publishing online to use in 'lineups'

roster = pd.read_csv('../data/roster.csv',
    header = 0)

public = roster[['Full Name','Goes By','Side','Active']]

public.to_csv('../public_data/roster.csv')