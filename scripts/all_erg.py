####################
##### Erg Doc #####
####################

# home directory
home_dir = "/Users/Rodd/Desktop/websites/coachroddtalebi.github.io/"
breaker = "\n\n\n==============================\n"



####################
# PACKAGES
from datetime import date, time, datetime, timedelta
import math
import pandas as pd
import os.path
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls



####################
# ROSTER
####################
# get roster names
roster = pd.read_csv(home_dir + 'data/roster.csv',
    header = 0)
names = roster.loc[roster['Active']=='Active'].loc[roster['Side']!='Coxswain','Full Name'].tolist()

print breaker, "Current Roster: \n", len(names), "athletes\n", names

####################
# MISC FUNCTIONS
####################
def convert_split(erg_split):
    '''
    read in erg_split as a string "00:00.0"
    process and output as a 'datetime' object (not just time)

    # Example:
    erg_split = "2:32.3"
    a=convert_split(erg_split)
    print(a.strftime('%M:%S.%f')[:-5])
    '''
    '''# first check if 0 or Nan
    if (type(erg_split)==float) & (math.isnan(erg_split)):
        print("value is nan, return nan")
        return(float("Nan"))
    else:
        pass
    '''
    #split should be string
    erg_min, other = erg_split.split(':')
    erg_sec, erg_Msec = other.split('.')
    
    erg_min = int(erg_min)
    erg_sec = int(erg_sec)
    erg_Msec = int(float(erg_Msec)/10.0*1000000)
    return(datetime(year=2017,month=1,day=1,minute=erg_min, second=erg_sec, microsecond=erg_Msec))


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


def get_watts(raw_split):
    '''
    Convert split, as string, into watts
    '''
    pace = convert_split(raw_split).time()
    pace = (pace.minute*60+pace.second+pace.microsecond/1000000.0) / 500
    watts = 2.80/pace**3
    return watts


def check_watts(row):
    '''
    Check a row to see if the rower inputed watts.
    If it doesn't see a number it will convert the ave split to watts

    Also check if Watts is 0
    '''
    #if type(row['Watts']) is not int:
    try:
        row['Watts'] = int(row['Watts'])
    except ValueError:
        row['Watts'] = int(get_watts(row['AveSplit']))
    if int(row['Watts']) == 0: #not a valid watt, so convert
        row['Watts'] = int(get_watts(row['AveSplit']))
    return row



####################
# FALL - 30min
####################
print breaker, "Reading and opening 30min data..."

scores30 = pd.read_csv(
    home_dir + 'data/30min.csv',
    header = 0, #header is in first line
    parse_dates = [0],
    infer_datetime_format = True
    )

# sort Names and Date
scores30 = scores30.sort_values(by=['Name', 'Timestamp'])

# find PRs
scores30['PR'] = 0
for name in names:
    if scores30.loc[scores30['Name']==name].shape[0] > 0:
        name_loc = scores30['Name']==name
        # get the PR
        pr_loc = scores30.loc[name_loc,'Meters'].argmax()
        scores30.loc[pr_loc,'PR'] = 1
    else:
        continue

# plotter ftn
def plot_30min_intervals(name):
    '''
    for the given name, create a plot for the time intervals: 10min, 20min, 30min
    
    Documentation for plotting:
    https://plot.ly/python/reference/#layout-yaxis

    Example:
    fig = plot_30min_intervals(name)
    py.iplot(fig, filename = name+'-30min')
    '''
    traces = []
    name_loc = scores30['Name']==name
    if sum(name_loc) == 0:
        print "No 30min data for", name
        return 0
    else:
        pass
    dates = scores30.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime().date()).tolist()

    for i in range(scores30.loc[name_loc].shape[0]):
        try:
            times = scores30.loc[name_loc,['10min','20min','30min','AveSplit']].iloc[i].apply(
                                                                                lambda x: convert_split(x))
        except ValueError:
            # sometimes the rowers input the data incorrectly
            print "Error with data point for", name
            print scores30.loc[name_loc,['10min','20min','30min','AveSplit']].iloc[i]
            continue

        trace = go.Scatter(
            x=[10,20,30],
            y=times.tolist()[:-1],
            line=dict(
                shape='spline'
                ),
            name=dates[i],
            hoverinfo='text',
            hovertext=dates[i].strftime('%b%d')+'<br>Ave: '+times[-1].strftime('%M:%S.%f')[:-5]
            )
        traces.append(trace)

    layout = go.Layout(
        title = "30min Piece - " + name,
        xaxis=dict(
            title="Minutes"
            ),
        yaxis=dict(
            title="Ave Split",
            tickformat='%M:%S.%f'
            )
        )
    
    return go.Figure(data=traces, layout=layout)


####################
# get scores
for name in names:
    print "\n", name
    fig = plot_30min_intervals(name)
    if fig != 0:
        link = py.plot(fig, filename = name+'-30min', auto_open=False)
        print tls.get_embed(link)



####################
# FALL - 6km
####################
print breaker, "Reading and opening 6km data..."

# get 6km piece scores
scores6k = pd.read_csv(
    home_dir + 'data/6k.csv',
    header = 0, #header is in first line
    parse_dates = [0],
    infer_datetime_format = True
    )

# sort Names and Date
scores6k = scores6k.sort_values(by=['Name', 'Timestamp'])

# get watts 
scores6k = scores6k.apply(lambda x: check_watts(x), axis=1)

# find PRs with watts
scores6k['PR'] = 0
for name in names:
    if scores6k.loc[scores6k['Name']==name].shape[0] > 0:
        name_loc = scores6k['Name']==name
        # get the PR
        pr_loc = scores6k.loc[name_loc,'Watts'].argmax()
        scores6k.loc[pr_loc,'PR'] = 1  
    else:
        continue

# plotter ftn
def plot_6k_intervals(name):
    '''
    take in a name, and find all 6k scores
    plot each erg test individually over the time steps: each 1km interval
    if the data was not properly entered (no complete data for each 1km), the don't plot
    
    Example
    fig = plot_6k_intervals(name)
    py.iplot(fig, filename = name + '-6km')
    '''
    traces = []
    name_loc = scores6k['Name']==name
    if sum(name_loc) == 0:
        print "No 6km data for", name
        return 0
    else:
        pass
    dates = scores6k.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime().date()).tolist()

    for i in range(scores6k.loc[name_loc].shape[0]):
        # check to see if 1200m interval was submited instead of 1000m
        try:
            if scores6k.loc[name_loc,['4000m / 4800m']].iloc[i].isnull().any(): #2000m...because Suhm was dumb
                distance_interval = [2000,4000,6000]
                times = scores6k.loc[name_loc,['1000m / 1200m','2000m / 2400m','3000m / 3600m','AveSplit']].iloc[i].apply(
                                                                                                                        lambda x: convert_split(x))
            elif scores6k.loc[name_loc,['6000m / _']].iloc[i].isnull().any():
                distance_interval = [1200,2400,3600,4800,6000]
                times = scores6k.loc[name_loc,['1000m / 1200m','2000m / 2400m','3000m / 3600m', '4000m / 4800m', '5000m / 6000m', 'AveSplit']].iloc[i].apply(
                                                                                                                        lambda x: convert_split(x))
            else:
                distance_interval = [1000,2000,3000,4000,5000,6000]
                times = scores6k.loc[name_loc,['1000m / 1200m','2000m / 2400m','3000m / 3600m', '4000m / 4800m', '5000m / 6000m', '6000m / _', 'AveSplit']].iloc[i].apply(
                                                                                                                        lambda x: convert_split(x))
        except ValueError:
            print "Error with 6km erg test for", name
            print scores6k.loc[name_loc,['1000m / 1200m','2000m / 2400m','3000m / 3600m', '4000m / 4800m', '5000m / 6000m', '6000m / _', 'AveSplit']].iloc[i]
            continue

        trace = go.Scatter(
            x=distance_interval,
            y=times.tolist()[:-1],
            line=dict(
                shape='spline'
                ),
            name=dates[i],
            hoverinfo='text',
            hovertext=dates[i].strftime('%b%d')+'<br>Ave: '+times[-1].strftime('%M:%S.%f')[:-5]
            )
        traces.append(trace)

    layout = go.Layout(
        title = "6km Test - " + name,
        xaxis=dict(
            title="Meters"
            ),
        yaxis=dict(
            title="Ave Split",
            tickformat='%M:%S.%f'
            )
        )
    
    return go.Figure(data=traces, layout=layout)


####################
# get scores
for name in names:
    print "\n", name
    fig = plot_6k_intervals(name)
    if fig != 0:
        link = py.plot(fig, filename = name+'-6km', auto_open=False)
        print tls.get_embed(link)



####################
# FALL - Weight Adjusted 6km
####################
print breaker, "Corrected 6km data for Weight Adjusted Scores..."

# read in weights for each rower
weights = pd.read_csv(
    home_dir + 'data/weight.csv',
    header = 0, #header is in first line
    parse_dates = [0],
    infer_datetime_format = True
    )

# sort Names and Date
weights = weights.sort_values(by=['Name', 'Timestamp'])

# get dates from Timestamp for 6km and Weights
scores6k['Date'] = scores6k['Timestamp'].apply(lambda x: x.date())
weights['Date'] = weights['Timestamp'].apply(lambda x: x.date())

'''
Wf = [body weight in lbs / 270] raised to the power .222
Corrected time = Wf x actual time (seconds)
Corrected distance = actual distance / Wf
'''
def corrected(weight, split=None, distance=None):
    '''
    Read in weight and split or distance and adjust the score.
    
    Here is method recommended online (Concept2?):
    Wf = [body weight in lbs / 270] raised to the power .222
    Corrected time = Wf x actual time (seconds)
    Corrected distance = actual distance / Wf
    
    * split should be read in as string 00:00.0
      ...output will be the same
    * distance should be in meters
    * weight in lbs as float

    EXAMPLE
    corrected(weight=171.2, split="2:11.6")
    '''
    wf = (weight/270.0)**(2/9.0)
    
    if split is not None:
        pace = convert_split(split).time()
        pace = (pace.minute*60+pace.second+pace.microsecond/1000000.0) #to seconds
        corr_split = round(wf * pace,1)
        
        # now reformat from seconds to string
        minu = int(math.floor(corr_split/60.0))
        sec = int(math.floor(corr_split%60))
        micro = int(round((corr_split%1)*10))
        
        # put it all together
        corr_split = str(minu)+":"+str(sec)+"."+str(micro) 
    else:
        corr_split = None
    
    if distance is not None:
        corr_distance = distance / wf
    else:
        corr_distance = None
    
    return corr_split, corr_distance

# Adjust each 6k score with rower's weight on that day
scores6k['CorrSplit'] = "00:00.0"
for index, row in scores6k.iterrows():
    loc = (weights['Name']==row['Name']) & (weights['Date']==row['Date'])
    if sum(loc) == 1: #then there is an instance
        weight = weights.loc[loc,'Weight (lbs)']
        split = row['AveSplit']
        corr_split, _ = corrected(weight=weight, split=split)
        scores6k.loc[index,'CorrSplit'] = corr_split
    elif sum(loc) > 1:
        print "THERE IS A DUPLICATE WEIGHT FOR" + weights.loc[loc,'Name']
    else:
        print "Missing weight data for", row['Name'], " on ", row['Date']
        continue



####################
# SPRING - 4x10
####################
print breaker, "Reading and opening 4x10' data..."

scores4 = pd.read_csv(
    home_dir + "data/4x10.csv",
    header = 0,
    parse_dates = [0],
    infer_datetime_format = True
    )

scores4 = scores4.sort_values(by=['Name', 'Timestamp'])
scores4.columns = ['Timestamp','Name','1m','1s','2m','2s','3m','3s','4m','4s','Meters','Ave']

def plot_4x10min_intervals(name):
    '''
    for the given name, create a plot for the time intervals:
    1st, 2nd, 3rd, 4th 10' piece

    Example:
    fig = plot_1500m_intervals(name)
    py.iplot(fig, filename = name+'-30min')
    '''
    traces = []
    name_loc = scores4['Name']==name
    if sum(name_loc) == 0:
        print "No 4x10min data for", name
        return 0
    else:
        pass
    dates = scores4.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime().date()).tolist()
    for i in range(scores4.loc[name_loc].shape[0]):
        try:
            times = scores4.loc[name_loc,['1s','2s','3s','4s','Ave']].iloc[i].apply(
                                                                                lambda x: convert_split(x))
        except ValueError:
            # sometimes the rowers input the data incorrectly
            print "Error with 4x10min data point for", name
            print scores4.loc[name_loc,['1s','2s','3s','4s','Ave']].iloc[i]
            continue

        meters = scores4.loc[name_loc,'Meters'].iloc[i]
        trace = go.Scatter(
            x=[1,2,3,4],
            y=times.tolist()[:-1],
            line=dict(
                shape='spline'
                ),
            name=dates[i],
            hoverinfo='text',
            hovertext=dates[i].strftime('%b%d')+'<br>Ave: '+times[-1].strftime('%M:%S.%f')[:-5]+'<br>Meters: '+str(meters)
            )
        traces.append(trace)

    layout = go.Layout(
        title = "4x10min Pieces - " + name,
        xaxis=dict(
            title="10min Piece"
            ),
        yaxis=dict(
            title="Ave Split",
            tickformat='%M:%S.%f'
            )
        )
    
    return go.Figure(data=traces, layout=layout)


####################
# get scores
for name in names:
    print "\n", name
    fig = plot_4x10min_intervals(name)
    if fig != 0:
        link = py.plot(fig, filename = name+'-4x10min', auto_open=False)
        print tls.get_embed(link)



####################
# SPRING - 5x1500m
####################
print breaker, "Reading and opening 5x1500m data..."

scores5 = pd.read_csv(
    home_dir + "data/5x1500m.csv",
    header = 0,
    parse_dates = [0],
    infer_datetime_format = True
    )

scores5 = scores5.sort_values(by=['Name', 'Timestamp'])
scores5.columns = ['Timestamp','Name','1','2','3','4','5','Ave']

def plot_1500m_intervals(name):
    '''
    for the given name, create a plot for the time intervals:
    1st, 2nd, 3rd, 4th, 5th 1500m

    Example:
    fig = plot_1500m_intervals(name)
    py.iplot(fig, filename = name+'-30min')
    '''
    traces = []
    name_loc = scores5['Name']==name
    if sum(name_loc) == 0:
        print "No 5x1500m data for", name
        return 0
    else:
        pass
    dates = scores5.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime().date()).tolist()
    for i in range(scores5.loc[name_loc].shape[0]):
        try:
            times = scores5.loc[name_loc,['1','2','3','4','5','Ave']].iloc[i].apply(
                                                                                lambda x: convert_split(x))
        except ValueError:
            # sometimes the rowers input the data incorrectly
            print "Error with 1500m data point for", name
            print scores5.loc[name_loc,['1','2','3','4','5','Ave']].iloc[i]
            continue

        trace = go.Scatter(
            x=[1,2,3,4,5],
            y=times.tolist()[:-1],
            line=dict(
                shape='spline'
                ),
            name=dates[i],
            hoverinfo='text',
            hovertext=dates[i].strftime('%b%d')+'<br>Ave: '+times[-1].strftime('%M:%S.%f')[:-5]
            )
        traces.append(trace)

    layout = go.Layout(
        title = "5x1500m Pieces - " + name,
        xaxis=dict(
            title="1500m Piece"
            ),
        yaxis=dict(
            title="Ave Split",
            tickformat='%M:%S.%f'
            )
        )
    
    return go.Figure(data=traces, layout=layout)


####################
# get scores
for name in names:
    print "\n", name
    fig = plot_1500m_intervals(name)
    if fig != 0:
        link = py.plot(fig, filename = name+'-5x1500m', auto_open=False)
        print tls.get_embed(link)



####################
# SPRING - 2km
####################
print breaker, "Reading and opening 2km data..."

# get 6km piece scores
scores2k = pd.read_csv(
    home_dir + 'data/2k.csv',
    header = 0, #header is in first line
    parse_dates = [0],
    infer_datetime_format = True
    )
scores2k = scores2k.dropna(how="all")

# sort Names and Date
scores2k = scores2k.sort_values(by=['Name', 'Timestamp'])

# get watts 
scores2k = scores2k.apply(lambda x: check_watts(x), axis=1)

# find PRs with watts
scores2k['PR'] = 0
for name in names:
    if scores2k.loc[scores2k['Name']==name].shape[0] > 0:
        name_loc = scores2k['Name']==name
        # get the PR
        pr_loc = scores2k.loc[name_loc,'Watts'].argmax()
        scores2k.loc[pr_loc,'PR'] = 1  
    else:
        continue

# plotter ftn
def plot_2k_intervals(name):
    '''
    take in a name, and find all 2k scores
    plot each erg test individually over the time steps: each 500m interval
    if the data was not properly entered (no complete data for each 500m), then don't plot
    
    Example
    fig = plot_2k_intervals(name)
    py.iplot(fig, filename = name + '-2km')
    '''
    traces = []
    name_loc = scores2k['Name']==name
    if sum(name_loc) == 0:
        print "No 2km data for", name
        return 0
    else:
        pass
    dates = scores2k.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime().date()).tolist()

    for i in range(scores2k.loc[name_loc].shape[0]):
        # check to see if 400m interval was submited instead of 500m
        try:
            if scores2k.loc[name_loc,['_ / 2000m']].iloc[i].isnull().any(): #correctly did 500m split
                distance_interval = [500,1000,1500,2000]
                times = scores2k.loc[name_loc,['500m / 400m','1000m / 800m','1500m / 1200m', '2000m / 1600m', 'AveSplit']].iloc[i].apply(lambda x: convert_split(x))
            else:
                distance_interval = [400,800,1200,1600,2000]
                times = scores2k.loc[name_loc,['500m / 400m','1000m / 800m','1500m / 1200m', '2000m / 1600m', '_ / 2000m', 'AveSplit']].iloc[i].apply(lambda x: convert_split(x))
        except ValueError:
            print "Error with 2km erg test for", name
            print scores2k.loc[name_loc,['500m / 400m','1000m / 800m','1500m / 1200m', '2000m / 1600m', '_ / 2000m', 'AveSplit']].iloc[i]
            continue

        trace = go.Scatter(
            x=distance_interval,
            y=times.tolist()[:-1],
            line=dict(
                shape='spline'
                ),
            name=dates[i],
            hoverinfo='text',
            hovertext=dates[i].strftime('%b%d')+'<br>Ave: '+times[-1].strftime('%M:%S.%f')[:-5]
            )
        traces.append(trace)

    layout = go.Layout(
        title = "2km Test - " + name,
        xaxis=dict(
            title="Meters"
            ),
        yaxis=dict(
            title="Ave Split",
            tickformat='%M:%S.%f'
            )
        )
    
    return go.Figure(data=traces, layout=layout)


####################
# get scores
for name in names:
    print "\n", name
    fig = plot_2k_intervals(name)
    if fig != 0:
        link = py.plot(fig, filename = name+'-2km', auto_open=False)
        print tls.get_embed(link)



####################
# SPRING - Weight Adjusted 2km
####################
scores2k['Date'] = scores2k['Timestamp'].apply(lambda x: x.date())
# Adjust each 6k score with rower's weight on that day
scores2k['CorrSplit'] = "00:00.0"
for index, row in scores2k.iterrows():
    loc = (weights['Name']==row['Name']) & (weights['Date']==row['Date'])
    if sum(loc) == 1: #then there is an instance
        weight = weights.loc[loc,'Weight (lbs)']
        split = row['AveSplit']
        corr_split, _ = corrected(weight=weight, split=split)
        scores2k.loc[index,'CorrSplit'] = corr_split
    elif sum(loc) > 1:
        print "THERE IS A DUPLICATE WEIGHT FOR" + weights.loc[loc]
    else:
        print "Missing weight data for", row['Name'], " on ", row['Date'] 
        continue



####################
# TIMELINE - for each individual rower
####################
print breaker, "Build Timeline for each rower..."

def plot_intervals(name):
    traces = []
    have_info = False

    # -------------
    # 30min trace
    if scores30.loc[scores30['Name']==name].shape[0] > 0:
        name_loc = scores30['Name']==name

        times = scores30.loc[name_loc,'AveSplit'].apply(lambda x: convert_split(x))
        dates = scores30.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime())
        meters = [str(x[0])+"<br>"+str(x[1])+' meters' for _,x in scores30.loc[name_loc,['AveSplit','Meters']].iterrows()]
        
        trace = go.Scatter(
            x=dates,
            y=times,
            line=dict(
                shape='linear'#'spline'
                ),
            name="30min",
            hoverinfo='text', #the 'text' flags tells you to look at hovertext
            hovertext = meters
            )
        traces.append(trace)

        have_info = True
    else:
        print "no 30min pieces (Timeline) for " + name
        pass
      
    # -------------
    # 6km        
    if scores6k.loc[scores6k['Name']==name].shape[0] > 0:
        name_loc = scores6k['Name']==name        
        times = scores6k.loc[name_loc,'AveSplit'].apply(lambda x: convert_split(x))
        dates = scores6k.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime())
        watts = [str(x[0])+'<br>'+str(x[1])+' watts' for _,x in scores6k.loc[name_loc,['AveSplit','Watts']].iterrows()]
        
        trace = go.Scatter(
            x=dates,
            y=times,
            line=dict(
                shape='linear'#'spline'
                ),
            name="6k",
            hoverinfo='text', #the 'text' flags tells you to look at hovertext
            hovertext = watts
            )
        traces.append(trace)  

        have_info = True
        
        # -------------
        # 6km   CORRECTED     
        name_loc = (scores6k['Name']==name) & (scores6k['CorrSplit']!="00:00.0")
        if sum(name_loc) > 0:
            times = scores6k.loc[name_loc,'CorrSplit'].apply(lambda x: convert_split(x))
            dates = scores6k.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime())
            watts = [str(x[0])+"<br>"+str(x[1])+' watts' for _,x in scores6k.loc[name_loc,['CorrSplit','Watts']].iterrows()]

            trace = go.Scatter(
                x=dates,
                y=times,
                line=dict(
                    shape='linear'#'spline'
                    ),
                name="WeightAdj 6k",
                hoverinfo='text', #the 'text' flags tells you to look at hovertext
                hovertext = watts
                )
            traces.append(trace)
        else:
            print "not Corrected 6km data (Timeline) for " + name
            pass        
        
    else:
        print "no 6km data (Timeline) for " + name
        pass
    
    
    # -------------
    # 1500m trace
    if scores5.loc[scores5['Name']==name].shape[0] > 0:
        name_loc = scores5['Name']==name

        times = scores5.loc[name_loc,'Ave'].apply(lambda x: convert_split(x))
        dates = scores5.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime())
        ave = [str(x) for x in scores5.loc[name_loc,'Ave']]
        trace = go.Scatter(
            x=dates,
            y=times,
            line=dict(
                shape='linear'#'spline'
                ),
            name="5x1500m",
            hoverinfo='text', #the 'text' flags tells you to look at hovertext
            hovertext = ave
            )
        traces.append(trace)

        have_info = True

    else:
        print "no 1500m pieces (Timeline) for " + name
        pass

    
    # -------------
    # 4x10' trace
    if scores4.loc[scores4['Name']==name].shape[0] > 0:
        name_loc = scores4['Name']==name
        times = scores4.loc[name_loc,'Ave'].apply(lambda x: convert_split(x))
        dates = scores4.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime())
        #ave = [str(x) for x in scores4.loc[name_loc,'Ave']]
        ave = [str(x[0])+"<br>"+str(x[1])+' meters' for _,x in scores4.loc[name_loc,['Ave','Meters']].iterrows()]
        
        
        trace = go.Scatter(
            x=dates,
            y=times,
            line=dict(
                shape='linear'#'spline'
                ),
            name="4x10",
            hoverinfo='text', #the 'text' flags tells you to look at hovertext
            hovertext = ave
            )
        traces.append(trace)

        have_info = True
    else:
        print "no 4x10min pieces (Timeline) for " + name
        pass




    # -------------
    # 2km        
    if scores2k.loc[scores2k['Name']==name].shape[0] > 0:
        name_loc = scores2k['Name']==name        
        times = scores2k.loc[name_loc,'AveSplit'].apply(lambda x: convert_split(x))
        dates = scores2k.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime())
        watts = [str(x[0])+'<br>'+str(x[1])+' watts' for _,x in scores2k.loc[name_loc,['AveSplit','Watts']].iterrows()]
        
        trace = go.Scatter(
            x=dates,
            y=times,
            line=dict(
                shape='linear'#'spline'
                ),
            name="2k",
            hoverinfo='text', #the 'text' flags tells you to look at hovertext
            hovertext = watts
            )
        traces.append(trace)  

        have_info = True
        
        # -------------
        # 2km   CORRECTED     
        name_loc = (scores2k['Name']==name) & (scores2k['CorrSplit']!="00:00.0")
        if sum(name_loc) > 0:
            times = scores2k.loc[name_loc,'CorrSplit'].apply(lambda x: convert_split(x))
            dates = scores2k.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime())
            watts = [str(x[0])+"<br>"+str(x[1])+' watts' for _,x in scores2k.loc[name_loc,['CorrSplit','Watts']].iterrows()]

            trace = go.Scatter(
                x=dates,
                y=times,
                line=dict(
                    shape='linear'#'spline'
                    ),
                name="WeightAdj 2k",
                hoverinfo='text', #the 'text' flags tells you to look at hovertext
                hovertext = watts
                )
            traces.append(trace)

            have_info = True
        else:
            print "not Corrected 2km data (Timeline) for " + name
            pass        
        
    else:
        print "no 2km data (Timeline) for " + name
        pass






    
    #-------------------
    layout = go.Layout(
        title = "Erg Test Progression - "+ name,
        xaxis=dict(
            title="Date"
            ),
        yaxis=dict(
            title="Ave Split",
            tickformat='%M:%S.%f'
            )
        )
    
    return go.Figure(data=traces, layout=layout), have_info


####################
# get scores
for name in names:
    print "\n", name
    fig, have_info = plot_intervals(name)
    if have_info:
        link = py.plot(fig, filename = name+'-Timeline', auto_open=False)
        print tls.get_embed(link)
    else:
        print "there was nothing to plot"



####################
# GOLDEN CURVE - for each individual rower
####################
print breaker, "Build Golden Curve for each rower..."

def golden_curve(base2k=None, base6k=None):
    '''
    http://www.ergrowing.com/2k-erg-power-profile-calculator/

    Take in Watts for PR and output string split
    
    Use the PRs from the previous season to update the golden curve.
    
    Example:
    for Spring 2018, use 6k PR from Fall 2017 to create curve and then
    plot 2ks for the next season on top of it to see if there is progression
    '''
    # ASSUMING BASE VALUES ARE WATTS
    if base2k is not None:
        goal_10sec = get_split(1.73 * base2k)
        goal_60sec = get_split(1.53 * base2k)
        goal_2k = get_split(base2k)
        goal_6k = get_split(0.85 * base2k)
        goal_60min = get_split(0.76 * base2k)
    
    elif base6k is not None:
        goal_10sec = get_split(1.73/0.85 * base6k)
        goal_60sec = get_split(1.53/0.85 * base6k)
        goal_2k = get_split(1/0.85 * base6k)
        goal_6k = get_split(base6k)
        goal_60min = get_split(0.76/0.85 * base6k)
        
    else:
        print("ERROR: no Watts given")
    
    return(goal_10sec, goal_60sec, goal_2k, goal_6k, goal_60min)

# assume PRs already scored
def plot_golden_curve(name, season):
    '''
    Use data from the previous season to build a Golden Curve...
    * in Spring, use Fall's 6km scores
    * in Fall, use Spring's 2km scores

    EXAMPLE:
    fig = plot_golden_curve(name)
    py.iplot(fig, filename = name+'-GoldCurve')
    '''

    if season == "Spring":
        name_loc = (scores6k['Name']==name) & (scores6k['PR']==1)
        if sum(name_loc)==1:
            watts6k = scores6k.loc[name_loc, 'Watts']
        else:
            print "ERROR: there are more than 1 (or 0) PR flags for " + name
            return 0
        
        goals_str = list(golden_curve(base6k=watts6k))

    elif season == "Fall":
        name_loc = (scores2k['Name']==name) & (scores2k['PR']==1)
        if sum(name_loc)==1:
            watts2k = scores2k.loc[name_loc, 'Watts']
        else:
            print "ERROR: there are more than 1 (or 0) PR flags for " + name
            return 0
        
        goals_str = list(golden_curve(base2k=watts2k))

    else: # given wrong season
        print "ERROR: Wrong Season entered; must be Spring or Fall..."
        return 0

    goals_split = [convert_split(x) for x in goals_str]
    
    # get time
    # 2k
    split = goals_split[2]
    split = timedelta(minutes=split.minute, seconds=split.second, microseconds=split.microsecond)
    pace = (split*4).total_seconds()
    time_2k = pace/60.0

    # 6k
    split = goals_split[3]
    split = timedelta(minutes=split.minute, seconds=split.second, microseconds=split.microsecond)
    pace = (split*12).total_seconds()
    time_6k = pace/60.0#now in minutes
    
    display=[] #info for hoverbox
    for i, test in enumerate(["10sec", "60sec", "2k", "6k", "60min"]):
        display.append(test + "<br>" + goals_str[i])
        
    trace = go.Scatter(
        x=[10/60.0, 1.0, time_2k, time_6k, 60],
        y=[1.73,1.53,1.00,.85,.76],
        line=dict(
            shape='spline'
            ),
        name=name,
        hoverinfo='text', #the 'text' flags tells you to look at hovertext
        hovertext = display
        )

    layout = go.Layout(
        title = "Golden Curve - " + name,
        xaxis=dict(
            title="Minutes"
            ),
        yaxis=dict(
            title="%of 2k Watts"
            )
        )
    return go.Figure(data=[trace], layout=layout)


####################
# get scores
for name in names:
    print "\n", name
    fig = plot_golden_curve(name, "Spring") #which season it currently is
    if fig != 0:
        link = py.plot(fig, filename = name+'-GoldCurve', auto_open=False)
        print tls.get_embed(link)








####################
####################
# COACHES DASHBOARD
####################
####################
print breaker, "Get plots for Coaches' Dashboard..."



####################
# 30min Averages
print "\n30min Averages"
traces=[]
for name in names:
    name_loc = (scores30['Name']==name) & (scores30['PR']==1)
    if sum(name_loc)==1:
        dates = scores30.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime().date()).tolist()
    else:
        print "There was a problem with the number of 30min PRs for ", name
        continue

    try:
        times = scores30.loc[name_loc,['10min','20min','30min','AveSplit']].iloc[0].apply(
                                                                            lambda x: convert_split(x))
    except ValueError:
        # sometimes the rowers input the data incorrectly
        print "error with data point"
        print scores30.loc[name_loc,['10min','20min','30min','AveSplit']]
        continue

    trace = go.Scatter(
        x=[10,20,30],
        y=times.tolist()[:-1],
        line=dict(
            shape='spline'
            ),
        name=name,
        hoverinfo='text',
        hovertext=dates[0].strftime('%b%d')+'<br>Ave: '+times[-1].strftime('%M:%S.%f')[:-5]
        )
    traces.append(trace)

    layout = go.Layout(
        title = "10min Splits",
        xaxis=dict(
            title="Minutes"
            ),
        yaxis=dict(
            title="Ave Split",
            tickformat='%M:%S.%f'
            )
        )


####################
# get plot
fig = go.Figure(data=traces, layout=layout)
link = py.plot(fig, filename = '30minPRave', auto_open=False)
print tls.get_embed(link)



####################
# 30min Timeline
print "\n30min Timeline"
traces=[]
for name in names:
    name_loc = scores30['Name']==name
    if sum(name_loc)>0:
        times = scores30.loc[name_loc,'AveSplit'].apply(lambda x: convert_split(x))
        dates = scores30.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime())
        meters = [name+"<br>"+str(x)+' meters' for x in scores30.loc[name_loc,'Meters']]
        
        trace = go.Scatter(
            x=dates,
            y=times,
            line=dict(
                shape='linear'#'spline'
                ),
            hoverinfo='text', #the 'text' flags tells you to look at hovertext
            name=name,
            hovertext = meters
            )
        traces.append(trace)
    else:
        print "No 30min scores to report for " + name

layout = go.Layout(
    title = "30min Timeline",
    xaxis=dict(
        title="Date"
        ),
    yaxis=dict(
        title="Ave Split",
        tickformat='%M:%S.%f'
        )
    )


####################
# get plot
fig = go.Figure(data=traces, layout=layout)
link = py.plot(fig, filename = '30min', auto_open=False)
print tls.get_embed(link)



####################
# 6k Averages PR
print "\n6km Averages"
traces=[]
for name in names:
    name_loc = (scores6k['Name']==name) & (scores6k['PR']==1)
    if sum(name_loc)==1:
        date = scores6k.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime().date()).tolist()
    else:
        print "Wrong number of PRs for ", name
        continue    

    try:
        if scores6k.loc[name_loc,['4000m / 4800m']].iloc[0].isnull().any(): #2000m...because Suhm was dumb
            distance_interval = [2000,4000,6000]
            times = scores6k.loc[name_loc,['1000m / 1200m','2000m / 2400m','3000m / 3600m','AveSplit']].iloc[0].apply(
                                                                                                                    lambda x: convert_split(x))
        elif scores6k.loc[name_loc,['6000m / _']].iloc[0].isnull().any():
            distance_interval = [1200,2400,3600,4800,6000]
            times = scores6k.loc[name_loc,['1000m / 1200m','2000m / 2400m','3000m / 3600m', '4000m / 4800m', '5000m / 6000m', 'AveSplit']].iloc[0].apply(
                                                                                                                    lambda x: convert_split(x))
        else:
            distance_interval = [1000,2000,3000,4000,5000,6000]
            times = scores6k.loc[name_loc,['1000m / 1200m','2000m / 2400m','3000m / 3600m', '4000m / 4800m', '5000m / 6000m', '6000m / _', 'AveSplit']].iloc[0].apply(
                                                                                                                    lambda x: convert_split(x))
    except ValueError:
        print "Error with 6km erg test for", name
        print scores6k.loc[name_loc,['1000m / 1200m','2000m / 2400m','3000m / 3600m', '4000m / 4800m', '5000m / 6000m', '6000m / _', 'AveSplit']].iloc[0]
        continue

    trace = go.Scatter(
        x=distance_interval,#[1000,2000,3000,4000,5000,6000],
        y=times.tolist()[:-1],
        line=dict(
            shape='spline'
            ),
        name=name,
        hoverinfo='text',
        hovertext=date[0].strftime('%b%d')+'<br>Ave: '+times[-1].strftime('%M:%S.%f')[:-5]
        )
    traces.append(trace)

    layout = go.Layout(
        title = "1km Splits",
        xaxis=dict(
            title="Meters"
            ),
        yaxis=dict(
            title="Ave Split",
            tickformat='%M:%S.%f'
            )
        )


####################
# get plot
fig = go.Figure(data=traces, layout=layout)
link = py.plot(fig, filename = '6kmPRave', auto_open=False)
print tls.get_embed(link)



####################
# 6km Timeline
print "\n6km Timeline"
traces=[]
for name in names:
    name_loc = scores6k['Name']==name
    if sum(name_loc)>0:
        times = scores6k.loc[name_loc,'AveSplit'].apply(lambda x: convert_split(x))
        dates = scores6k.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime())
        meters = [name+"<br>"+str(x)+' watts' for x in scores6k.loc[name_loc,'Watts']]
        
        trace = go.Scatter(
            x=dates,
            y=times,
            line=dict(
                shape='linear'
                ),
            hoverinfo='text', #the 'text' flags tells you to look at hovertext
            name=name,
            hovertext = meters
            )
        traces.append(trace)
    else:
        print "No 6km scores to report for " + name

layout = go.Layout(
    title = "6km Timeline",
    xaxis=dict(
        title="Date"
        ),
    yaxis=dict(
        title="Ave Split",
        tickformat='%M:%S.%f'
        )
    )


####################
# get plot
fig = go.Figure(data=traces, layout=layout)
link = py.plot(fig, filename = '6km', auto_open=False)
print tls.get_embed(link)



####################
# 6km CORRECTED Timeline
print "\n6km Corrected Timeline"
traces=[]
for name in names:
    name_loc = (scores6k['Name']==name) & (scores6k['CorrSplit']!="00:00.0")
    if sum(name_loc)>0:
        times = scores6k.loc[name_loc,'CorrSplit'].apply(lambda x: convert_split(x))
        dates = scores6k.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime())
        meters = [name+"<br>"+str(x)+' watts' for x in scores6k.loc[name_loc,'Watts']]
        
        trace = go.Scatter(
            x=dates,
            y=times,
            line=dict(
                shape='linear'#'spline'
                ),
            hoverinfo='text', #the 'text' flags tells you to look at hovertext
            name=name,
            hovertext = meters
            )
        traces.append(trace)
    else:
        print "No CORRECTED 6km scores to report for " + name

layout = go.Layout(
    title = "CORRECTED 6km Timeline",
    xaxis=dict(
        title="Date"
        ),
    yaxis=dict(
        title="Ave Split",
        tickformat='%M:%S.%f'
        )
    )


####################
# get plot
fig = go.Figure(data=traces, layout=layout)
link = py.plot(fig, filename = 'CORR-6km', auto_open=False)
print tls.get_embed(link)



####################
# Weights Timeline
print "\nWeights"
traces = []
for name in names:
    name_loc = weights['Name']==name
    if sum(name_loc) > 0:
        display = [name+"<br>"+str(x) for x in weights.loc[name_loc, 'Weight (lbs)']]
        trace = go.Scatter(
            x=weights.loc[name_loc, 'Date'],
            y=weights.loc[name_loc, 'Weight (lbs)'],
            line=dict(
                shape='spline'
                ),
            name=name,
            hoverinfo='text', #the 'text' flags tells you to look at hovertext
            hovertext = display#weights.loc[name_loc, 'Weight (lbs)']
            )
        traces.append(trace)

layout = go.Layout(
    title = "Rowers Weight",
    xaxis=dict(
        title="Date"
        ),
    yaxis=dict(
        title="lbs"
        )
    )


####################
# get plot
fig = go.Figure(data=traces, layout=layout)
link = py.plot(fig, filename = 'Weights', auto_open=False)
print tls.get_embed(link)



####################
# Golden Curves
print "\nGolden Curves"
# assume PRs already scored
season = "Fall"
traces = []
for name in names:

    if season == "Spring":
        name_loc = (scores6k['Name']==name) & (scores6k['PR']==1)
        if sum(name_loc)==1:
            watts6k = scores6k.loc[name_loc, 'Watts']
        else:
            print "ERROR: there are more than 1 (or 0) PR flags for " + name
            continue
        goals_str = list(golden_curve(base6k=watts6k))

    elif season == "Fall":
        name_loc = (scores2k['Name']==name) & (scores2k['PR']==1)
        if sum(name_loc)==1:
            watts2k = scores2k.loc[name_loc, 'Watts']
        else:
            print "ERROR: there are more than 1 (or 0) PR flags for " + name
            continue
        goals_str = list(golden_curve(base2k=watts2k))

    else:
        # should never get here
        print "DIDN'T USE CORRECT SEASON"
        break

    goals_split = [convert_split(x) for x in goals_str]
    
    # get time
    # 2k
    split = goals_split[2]
    split = timedelta(minutes=split.minute, seconds=split.second, microseconds=split.microsecond)
    pace = (split*4).total_seconds()
    time_2k = pace/60.0

    # 6k
    split = goals_split[3]
    split = timedelta(minutes=split.minute, seconds=split.second, microseconds=split.microsecond)
    pace = (split*12).total_seconds()
    time_6k = pace/60.0#now in minutes
    
    display=[] #info for hoverbox
    for i, test in enumerate(["10sec", "60sec", "2k", "6k", "60min"]):
        display.append(name+"-"+test + "<br>" + goals_str[i])
        
    trace = go.Scatter(
        x=[10/60.0, 1.0, time_2k, time_6k, 60],
        y=[1.73,1.53,1.00,.85,.76],
        line=dict(
            shape='spline'
            ),
        name=name,
        hoverinfo='text', #the 'text' flags tells you to look at hovertext
        hovertext = display
        )
    
    traces.append(trace)

layout = go.Layout(
    title = "Golden Curve",
    xaxis=dict(
        title="Minutes"
        ),
    yaxis=dict(
        title="%of 2k Watts"
        )
    )


####################
# get plot
fig = go.Figure(data=traces, layout=layout)
link = py.plot(fig, filename = 'GoldCurve', auto_open=False)
print tls.get_embed(link)



####################
# 5x1500m ...most recent
print "\n5x1500m"
traces = []
scores5['Date'] = scores5['Timestamp'].apply(lambda x: x.to_datetime().date())
for name in names:
    name_loc = scores5['Name']==name
    if sum(name_loc) > 0:
        date = scores5.loc[name_loc,'Date'].max()
        date_loc = name_loc & (scores5['Date']==date)
    else:
        print("Not enough data for 5x1500m", name)
        continue
    
    assert sum(date_loc)==1, "uh, more than one data point for %s" % (name)
    
    times = scores5.loc[date_loc,['1','2','3','4','5','Ave']].iloc[0].apply(lambda x: convert_split(x))
    
    trace = go.Scatter(
        x=[1500,3000,4500,6000,7500],
        y=times.tolist()[:-1],
        line=dict(
            shape='spline'
            ),
        name=name,
        hoverinfo='text',
        hovertext=date.strftime('%b%d')+'<br>Ave: '+times[-1].strftime('%M:%S.%f')[:-5]
        )
    traces.append(trace)

layout = go.Layout(
    title = "Most Recent 5x1500m",
    xaxis=dict(
        title="1500m Piece"
        ),
    yaxis=dict(
        title="Ave Split",
        tickformat='%M:%S.%f'
        )
    )


####################
# get plot 
fig = go.Figure(data=traces, layout=layout)
link = py.plot(fig, filename = '5x1500 Recent', auto_open=False)
print tls.get_embed(link)



####################
# 4x10min ...most recent
print "\n4x10min"  
traces = []
scores4['Date'] = scores4['Timestamp'].apply(lambda x: x.to_datetime().date())
for name in names:
    name_loc = scores4['Name']==name
    if sum(name_loc) > 0:
        date = scores4.loc[name_loc,'Date'].max()
        date_loc = name_loc & (scores4['Date']==date)
    else:
        print("Not enough data for 4x10min", name)
        continue
    
    assert sum(date_loc)==1, "uh, more than one data point for %s" % (name)
    
    times = scores4.loc[date_loc,['1s','2s','3s','4s','Ave']].iloc[0].apply(lambda x: convert_split(x))
    meters = scores4.loc[date_loc,'Meters'].iloc[0]
    trace = go.Scatter(
        x=[1,2,3,4],
        y=times.tolist()[:-1],
        line=dict(
            shape='spline'
            ),
        name=name,
        hoverinfo='text',
        hovertext=date.strftime('%b%d')+'<br>Ave: '+times[-1].strftime('%M:%S.%f')[:-5]+'<br>Meters: '+str(meters)
        )
    traces.append(trace)

layout = go.Layout(
    title = "Most Recent 4x10m",
    xaxis=dict(
        title="4x10min Piece"
        ),
    yaxis=dict(
        title="Ave Split",
        tickformat='%M:%S.%f'
        )
    )


####################
# get plot  
fig = go.Figure(data=traces, layout=layout)
link = py.plot(fig, filename = '4x10 Recent', auto_open=False)
print tls.get_embed(link)




####################
# 2k Averages PR
print "\n2km Averages"
traces=[]
for name in names:
    name_loc = (scores2k['Name']==name) & (scores2k['PR']==1)
    if sum(name_loc)==1:
        date = scores2k.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime().date()).tolist()
    else:
        print "Wrong number of PRs for ", name
        continue

    # check to see if 400m interval was submited instead of 500m
    try:
        if scores2k.loc[name_loc,['_ / 2000m']].iloc[0].isnull().any(): #correctly did 500m split
            distance_interval = [500,1000,1500,2000]
            times = scores2k.loc[name_loc,['500m / 400m','1000m / 800m','1500m / 1200m', '2000m / 1600m', 'AveSplit']].iloc[0].apply(lambda x: convert_split(x))
        else:
            distance_interval = [400,800,1200,1600,2000]
            times = scores2k.loc[name_loc,['500m / 400m','1000m / 800m','1500m / 1200m', '2000m / 1600m', '_ / 2000m', 'AveSplit']].iloc[0].apply(lambda x: convert_split(x))
    except ValueError:
        print "Error with 2km erg test for", name
        print scores2k.loc[name_loc,['500m / 400m','1000m / 800m','1500m / 1200m', '2000m / 1600m', '_ / 2000m', 'AveSplit']].iloc[0]
        continue


    trace = go.Scatter(
        x=distance_interval,#[500,1000,1500,2000],
        y=times.tolist()[:-1],
        line=dict(
            shape='spline'
            ),
        name=name,
        hoverinfo='text',
        hovertext=date[0].strftime('%b%d')+'<br>Ave: '+times[-2].strftime('%M:%S.%f')[:-5]+'<br>WgtAdj: '+times[-1].strftime('%M:%S.%f')[:-5]
        )
    traces.append(trace)

    layout = go.Layout(
        title = "500m Splits",
        xaxis=dict(
            title="Meters"
            ),
        yaxis=dict(
            title="Ave Split",
            tickformat='%M:%S.%f'
            )
        )


####################
# get plot
fig = go.Figure(data=traces, layout=layout)
link = py.plot(fig, filename = '2kmPRave', auto_open=False)
print tls.get_embed(link)




####################
# 2km Timeline
print "\n2km Timeline"
traces=[]
for name in names:
    name_loc = scores2k['Name']==name
    if sum(name_loc)>0:
        times = scores2k.loc[name_loc,'AveSplit'].apply(lambda x: convert_split(x))
        dates = scores2k.loc[name_loc,'Timestamp'].apply(lambda x: x.to_datetime())
        meters = [name+"<br>"+"WgtAdj: "+convert_split(x).strftime('%M:%S.%f')[:-5] for x in scores2k.loc[name_loc,'CorrSplit']]
        
        trace = go.Scatter(
            x=dates,
            y=times,
            line=dict(
                shape='linear'
                ),
            hoverinfo='text', #the 'text' flags tells you to look at hovertext
            name=name,
            hovertext = meters
            )
        traces.append(trace)
    else:
        print "No 2km scores to report for " + name

layout = go.Layout(
    title = "2km Timeline",
    xaxis=dict(
        title="Date"
        ),
    yaxis=dict(
        title="Ave Split",
        tickformat='%M:%S.%f'
        )
    )


####################
# get plot
fig = go.Figure(data=traces, layout=layout)
link = py.plot(fig, filename = '2km', auto_open=False)
print tls.get_embed(link)











