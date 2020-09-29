# Documentation

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Tinderbot](#tinderbot)
  * [Creating a Session](#creating-a-session)
  * [Settings](#settings)
    * [Scrapers Location](#scrapers-location)
  * [Actions](#actions)
    * [Logging in to Tinder](#logging-in-to-tinder)
    * [Liking Geomatches](#liking-geomatches)
    * [Disliking Geomatches](#disliking-geomatches)
    * [Superliking Geomatches](#superliking-geomatches)
    * [Get Matches](#getting-matches)
    * [Get Geomatches](#getting-geomatches)
    * [Storing (geo)Matches](#storing-geomatches)
* [Data Analysis](#data-analysis)

## Tinderbot
## Creating a Session
First thing you'll have to do is import Session from tinderbot.session and create an active session.</br>
In this session we can adjust settings or take actions, such as liking or scraping data.
```
from tinderbot.session import Session

session = Session()
```

## Settings
### Scrapers Location
This setting is only required when you want to reverse engineer the profiles location out of multiple scrapes.</br>
This latitude and longitude will be stored with the distance in the scraped profile. </br>
To get the latitude and longitude (location) of this profile you will need multiple scrapes from different locations.</br>
Then you can look for the intersections of the circles (distance) around your locations and know their location. (more or less)</br>
```
session.setScrapersLocation(latitude, longitude)
```
## Actions
### Logging in to Tinder
Logging in can be done in one of the following ways.
1. Using your Google-account: MAKE SURE YOU HAVE A VERIFIED EMAIL
2. Using your Facebook-account: MAKE SURE YOUR TINDER IS CONNECTED TO YOUR FACEBOOK
```
session.loginUsingGoogle(email, password)
session.loginUsingFacebook(email, password)
```
### Liking Geomatches
```
session.like()
```
**Optional parameters**</br>
```amount```: The amount of profiles that must get liked

### Disliking Geomatches
```
session.dislike()
```
**Optional parameters**</br>
```amount```: The amount of profiles that must get disliked

### Superliking Geomatches
```
session.superlike()
```
**Optional parameters**</br>
```amount```: The amount of profiles that must get superliked

### Getting Matches
Your matches can be divided into two categories:
1. New matches with whom you haven't exchanged messages with yet
2. Messaged matches with whom you have already interacted
```
new_matches = session.getNewMatches()    
old_matches = session.getMessagedMatches()
# or just get all matches at once
matches = session.getAllMatches()
```
**Note**: Loading your matches like this might take a while depending on how many matches you have.</br>
This is because the session will iterate through every match and all their images one by one.</br>
The best way reduce loading time is to store these matches at the first run as illustrated here: [Storing (geo)Matches](#storing-geomatches)</br>
and load them from there onwards in future runs.</br>

### Getting Geomatches
Geomatches are users that fulfill **your criteria** and you fullfill **their criteria**, such as distance, age and gender. </br>
This *first way of matching* if why we name these profiles *geomatches*.</br>
```
# get profile data (name, age, bio, images, ...)
geomatch = session.getGeomatch()
```
### Storing (geo)Matches
A profile also known as (geo)match can be stored locally. </br>
Storing data can be usefull for reducing runtime, for exampling when needing to fetch your matches,</br>
and for performing some data analysis on that data. More about data analysis can be found here: [Data Analysis](#data-analysis)</br>
```
matches = session.getAllMatches()
for match in matches:
   session.storeLocal(match)
   
geomatch = session.getGeomatch()
session.storeLocal(geomatch)
```


For now, 
1. Open the [quickstart_tinderbot.py](https://github.com/frederikme/TinderBot/blob/master/quickstart_tinderbot.py) from the tinderbot directory.
2. Fill in your credentials (email and password) to be able to login to Tinder.
3. Change the quickstart script to your needs.

If you want to scrape as much profiles as possible,</br>
then [scraper.py](https://github.com/frederikme/TinderBot/blob/master/scraper.py) will be suiting your needs better.

# Data Analysis
