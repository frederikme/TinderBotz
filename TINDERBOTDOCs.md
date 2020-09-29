# Tinderbot Documentation
Tinderbot exists around interacting with two types of users.</br>
1. ***Matches***</br>
Matches are profiles you have liked and whom have liked you back.</br>
You are now able to send them messages, gifs, songs, your social media and much more.</br>

2. ***Geomatches***</br>
Geomatches are users that fulfill **your criteria**, *such as distance, age and gender*, and by whom you fullfill **their criteria**.</br>
Seeing these profiles and thus '*breaking the first barrier of matching*' is why we name these profiles *geomatches*.</br>

<!-- TABLE OF CONTENTS -->
## Table of Contents
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
  * [Sending Messages](#sending-messages)
  * [Sending GIFS](#sending-gifs)
  * [Sending Songs](#sending-songs)
  * [Sending Socials](#sending-socials)
  * [Unmatching](#unmatching)
* [JUST LET ME START ALREADY YES PLS TY](#just-let-me-start-already-yes-pls-ty)

# Creating a Session
First thing you'll have to do is import Session from tinderbot.session and create an active session.</br>
In this session we can adjust settings or take actions, such as liking or scraping data.
```
from tinderbot.session import Session

session = Session()
```

# Settings
## Scrapers Location
This setting is only required when you want to reverse engineer the profiles location out of multiple scrapes.</br>
This latitude and longitude will be stored with the distance in the scraped profile. </br>
To get the latitude and longitude (location) of this profile you will need multiple scrapes from different locations.</br>
Then you can look for the intersections of the circles (distance) around your locations and know their location. (more or less)</br>
```
session.setScrapersLocation(latitude, longitude)
```
# Actions
## Logging in to Tinder
Logging in can be done in one of the following ways.
1. Using your Google-account: *Your email must be verified*
2. Using your Facebook-account: *Your Tinder must be connected to your Facebook*
```
session.loginUsingGoogle(email, password)
session.loginUsingFacebook(email, password)
```
## Liking Geomatches
```
session.like()
```
**Optional parameters**</br>
```amount```: The amount of profiles that must get liked.

## Disliking Geomatches
```
session.dislike()
```
**Optional parameters**</br>
```amount```: The amount of profiles that must get disliked.

## Superliking Geomatches
```
session.superlike()
```
**Optional parameters**</br>
```amount```: The amount of profiles that must get superliked.

## Getting Matches
Your matches can be divided into two categories:
1. New matches with whom you haven't exchanged messages with yet.
2. Messaged matches with whom you have already interacted.
These matches will be a list of objects of the [class Match](https://github.com/frederikme/TinderBot/blob/master/tinderbot/helpers/match.py) which is a childclass of the [class Geomatch](https://github.com/frederikme/TinderBot/blob/master/tinderbot/helpers/geomatch.py).
```
new_matches = session.getNewMatches()    
old_matches = session.getMessagedMatches()

# or just get all matches at once
matches = session.getAllMatches()
```
**Note**: Loading your matches like this might take a while depending on how many matches you have.</br>
This is because the session will iterate through every match and all their images one by one.</br>
The best way to reduce loading time is to store these matches at the first run as illustrated here: [Storing (geo)Matches](#storing-geomatches)</br>
and load them from there in future runs.</br>

## Getting Geomatches
Get data *name, age, bio, images...* of the displayed geomatch and store it inside an object of the [class Geomatch()](https://github.com/frederikme/TinderBot/blob/master/tinderbot/helpers/geomatch.py).
```
geomatch = session.getGeomatch()
```
## Storing (geo)Matches
Every profile, also known as a (geo)match, can be stored locally. </br>
Storing data can be useful for reducing runtime, for exampling when needing to fetch your matches,</br>
and for performing some data analysis. More about data analysis can be found here: [Data Analysis](#data-analysis)</br>
```
matches = session.getAllMatches()
for match in matches:
   session.storeLocal(match)
   
geomatch = session.getGeomatch()
session.storeLocal(geomatch)
```
## Sending Messages
Messages can be sent to matches.</br>
[Scrape your matches](#getting-matches) or fetch them from your locally stored json file.</br>
 ```
id = match.getChatID()
name = match.getName()
 
pickup_line = "Hey {}, you got look exactly like my future wife. ;)".format(name)

# send them a unique pick up line with their personal name
session.sendMessage(chatid=id, message=pickup_line)
```
## Sending GIFS
GIFS can be sent to matches.</br>
[Scrape your matches](#getting-matches) or get them from your locally stored json file.</br>
</br>
Sending a GIF will open the correct chat with your match, browse for the gif and send the first one that's being displayed.
```
id = match.getChatID()
session.sendGif(chatid=id, gifname="pizza")
```
## Sending Songs
Songs can be sent to matches.</br>
[Scrape your matches](#getting-matches) or get them from your locally stored json file.</br>
</br>
Sending a song will open the correct chat with your match, browse for the song and send the first one that's being displayed.
```
id = match.getChatID()
session.sendSong(chatid=id, songname="cutiepie")
```
## Sending Socials
Socials can be sent to matches.</br>
[Scrape your matches](#getting-matches) or get them from your locally stored json file.</br>
</br>
There are different types of socials. [Click here](https://github.com/frederikme/TinderBot/blob/master/tinderbot/helpers/socials.py) to see what types of social media or available.</br> 
```
id = match.getChatID()
session.sendSocials(chatid=id, media=Socials.INSTAGRAM, value="Teeti.fm")
```
## Unmatching
You can unmatch a match. **BUT** think twice before you do. Once you unmatch, there is no going back.
```
id = match.getChatID()
session.unMatch(chatid=id)
```

# ***JUST LET ME START ALREADY YES PLS TY***
If you feel like you just want to dive right into the code and get started right away, this is where you need to be. :) </br>

1. Open the [quickstart_tinderbot.py](https://github.com/frederikme/TinderBot/blob/master/quickstart_tinderbot.py) from the tinderbot directory.
2. Fill in your credentials (email and password) to be able to login to Tinder.
3. Change the quickstart script to your needs.
4. Run the code.

If you want to scrape as much *geomatches* as possible,</br>
then [scraper.py](https://github.com/frederikme/TinderBot/blob/master/scraper.py) will be suiting your needs better.
