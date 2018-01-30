import pandas as pd
import math

def get_split(raw_watts):
    '''
    Convert watts into erg split as 'string'
    ...use convert_split() to convert to datetime
    '''
    pace = (2.80/float(raw_watts))**(1/3.0) #now in seconds
    pace = round(pace*500,1)
    
    # now reformat from seconds to string
    minu = int(math.floor(pace/60.0))
    sec = int(math.floor(pace%60))
    micro = int(round((pace%1)*10))
    
    return str(minu)+":"+str(sec)+"."+str(micro)



def golden_curve(base10=None, base60=None):
    '''
    http://www.ergrowing.com/2k-erg-power-profile-calculator/

    Take in Watts for PR and output string split
    
    Use the PRs from the previous season to update the golden curve.
    
    Example:
    for Spring 2018, use 6k PR from Fall 2017 to create curve and then
    plot 2ks for the next season on top of it to see if there is progression
    '''
    # ASSUMING BASE VALUES ARE WATTS
    if base10 is not None:
        goal_10sec = get_split(base10)
        goal_60sec = get_split(1.53/1.73 * base10)
        goal_2k = get_split(1/1.73 * base10)
        goal_6k = get_split(0.85/1.73 * base10)
        goal_60min = get_split(0.76/1.73 * base10)
    
    elif base60 is not None:
        goal_10sec = get_split(1.73/1.53 * base60)
        goal_60sec = get_split(base60)
        goal_2k = get_split(1/1.53 * base60)
        goal_6k = get_split(base60)
        goal_60min = get_split(0.76/1.53 * base60)
        
    else:
        print("ERROR: no Watts given")
    
    return(goal_10sec, goal_60sec, goal_2k, goal_6k, goal_60min)


home_dir = "/Users/Rodd/Desktop/websites/coachroddtalebi.github.io/"
scores = pd.read_csv(
    home_dir + 'data/MaxWattTest.csv',
    header = 0 #header is in first line
    )

for _, row in scores.iterrows():
    print "\n", row['Name']
    print "2k from 10\"", golden_curve(base10=row['Best 10"'])[2]
    print "2k from 60\"", golden_curve(base60=row['60"'])[2]


