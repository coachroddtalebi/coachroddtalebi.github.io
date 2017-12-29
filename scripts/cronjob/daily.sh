#!/bin/sh

#------------------
# a simply shell script for updating website
# steps:
# * use driveAPI.py to download latest attendance, absence, injury
# * clean up attendance with update_attendance.py
# * update roster with update_roster.py
# * push those updated csv to github

#-----------------

python /Users/Rodd/Desktop/websites/roddtalebi.github.io/scripts/driveAPI.py "Attendance"
python /Users/Rodd/Desktop/websites/roddtalebi.github.io/scripts/driveAPI.py "Absence"
python /Users/Rodd/Desktop/websites/roddtalebi.github.io/scripts/driveAPI.py "Injury Report"
python /Users/Rodd/Desktop/websites/roddtalebi.github.io/scripts/update_attendance.py
python /Users/Rodd/Desktop/websites/roddtalebi.github.io/scripts/update_roster.py
git --git-dir=/Users/Rodd/Desktop/websites/roddtalebi.github.io/.git/ --work-tree=/Users/Rodd/Desktop/websites/roddtalebi.github.io/ add --all
git --git-dir=/Users/Rodd/Desktop/websites/roddtalebi.github.io/.git/ --work-tree=/Users/Rodd/Desktop/websites/roddtalebi.github.io/ commit -m "updating with daily attendance and roster check"
git --git-dir=/Users/Rodd/Desktop/websites/roddtalebi.github.io/.git/ --work-tree=/Users/Rodd/Desktop/websites/roddtalebi.github.io/ push https://roddtalebi:govdule3@github.com/roddtalebi/roddtalebi.github.io.git master
