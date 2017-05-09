# Outline for site structure
pushing to github (https://pages.github.com/)...GITHUB.IO IS STATIC...DOESN'T WORK WITH PHP

Steps to take:
Get all forms done.
Get Sample data off the forms.
Create scripts to clean and create visualizations in plotly.
Tie back into html and d3 already made.

## csv files
* Roster.csv - (GoogleForm Response) for each rower, detail out bio + accademic info + aggregated stats for easy call
* Attendance.csv - (GoogleForm Response) for each day, who didn't attend
* Attendance_Cleaned.csv - built off Attendance.csv, for each name (rows), says whether they attended or not (1 or 0) for each day (col)
* Absent.csv - (GoogleForm Response) pull responses to see if anyone is going to be absent in near future
	can apparnetly make calendar event from google form with a simple plugin (find from GoogleSheets) 
* Injury.csv - (GoogleForm Response) pull responses to see if anyone is injured or if there are updates on injury
	can i create calendar even but exclude injury updates?? maybe if the date feild is blank.
* 2k.csv - (GoogleForm Response) rowers submit their detailed times. Watts and splits
* 6k.csv - (GoogleForm Response) rowers submit their detailed times. Watts and splits
* 30min.csv - (GoogleForm Response) rowers submit their detailed times. Meters and splits.
* Fleet.csv - List of our fleet (include oars or make new csv for oars)

Others: maybe one for coach's notes?

## CRON Jobs
* Daily (5pm):
	- Download Attendance.csv from GoogleSheets;
	- Update Attendance_Cleaned.csv by adding new column for new day;
	- Download Absent.csv and Injury.csv from GoogleSheets;
	- Update Roster.csv with new attendance score, status (injured or absent) for each rower
	- push to github
* Every Erg Test:
	- Download the respective csv from GoogleSheets for the erg test
	- Update PR + Recent scores in Roster.csv
	- push to github

## Webpages
### Home page
* banner image (need to finish)
* workout calendar (think about putting in races and link to old race packets)
* link to water levels (need to find)
* weather calendar

### Schedule
* link to Google Calendar

### Roster
THINK ABOUT NOT LISTING THIS PUBLICLY. HAVE SEPERATE COACHES DASHBOARD WITH TEAM AVERAGES AND THEN ROSTER.
* image gallery of all rowers linking to their respective pages
 (skeleton of this is done. a lot of this is just filling it out by hand. finish individual pages first)

#### Individual Rower
* import data from Roster.csv for bio, accademic info, and aggregated stats
	(create original GoogleForm for all this. add new columns to GoogleSheets. create python script to fill out or update cells with attendance, pr scores, etc)
* import Injury.csv to display injury report in a table (i think this can be done on d3. need to also create GoogleForm for it)
* import Attendance_Cleaned.csv to track attendance (create python script to clean attendance, visualize with d3 or plotly)
* import 2k data to plot data every 500m (python and plotly to iframe. same for rest. but what to put on y-axis? fix the axis for all rowers)
	weight adjusted calc (http://www.concept2.com/indoor-rowers/training/calculators/weight-adjustment-calculator)
* import 6k data to plot data every 1000m
* import 30min data to plot data for every 10min
* import 2k PR (or recent) data from Roster to build watt curve. (http://www.ergrowing.com/2k-erg-power-profile-calculator/)

### Notes
May change this as this idea gets developed

#### Technique
* posts on technique
* recommended excercises on erg + on track + lifting

#### Blog
* blog posts for emails I send out to everyone
* just make these pages simple html. don't worry about having actual blog format. too much work...little return

#### Videos
link to youtube. get it to link to the new coach.roddtalebi@gmail.com account

### Lineups
see and build lineups

#### Builder
* link to GoogleSheets to write in final lineups for that date
* d3 code to build pseudo white board...uses Roster.csv and Fleet.csv

#### Viewer
* iframe of the GoogleSheets of final lineups
* maybe put in iframe for weather and water level reports

### Forms
link to all the GoogleForms: Attendance, Absent, Injury Report, 2k, 6k, 30min, 60min

### Data
link to the GoogleSheets folder for all the data

### GroupMe
link to the groupme


## Other ideas
Seperate webpage into 'Rowers Public Page' where we can also have 'recruit' info. and then have another page for 'Coachs Dashboard'.

Coach's Dashboard
* roster for every rower
* setting lineups (maybe also make available to rowers to play with but more simple version)
* also can have an overview page for team stats and averages
* maybe also have a link to fill out Coach's Notes to make notes on what they can work on...have that link to the individual rowers page as well.
* maybe share this page with the coxswains...maybe not at the beginning of the year but everything leading up to it.
