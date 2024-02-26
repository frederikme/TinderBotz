# Tinderbotz Documentation
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
  * [Logging in to Tinder](#logging-in-to-tinder)
* [Settings](#settings)
  * [Custom Location](#custom-location)
  * [Email Notifications](#email-notifications)
  * [Distance Range](#distance-range)
  * [Age Range](#age-range)
  * [Sexuality](#sexuality)
  * [Global](#global)
* [Actions](#actions)
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
* [Getting Started](#just-let-me-start-already-yes-pls-ty)

# Creating a Session
First thing you'll have to do is import Session from tinderbot.session and create an active session.</br>
In this session we can adjust settings or take actions, such as liking or scraping data.
```
from tinderbot.session import Session

session = Session()
```
**Optional parameters**</br>
`headless`: *boolean*</br>
`store_session`: *boolean*</br>
`proxy`: *string*</br>

**Example usage**</br>
***headless*** might not work properly, so recommended to leave it on False. </br>
***store_session*** will store your cookies in a directory, so next time you don't need to login again. </br>
***proxy*** can be added using IP:PORT or HOST:PORT </br>
```
session = Session(headless=False, store_session=True, proxy="23.23.23.23:3128") 
```

## Logging in to Tinder
Logging in can be done in one of the following ways.
1. Using your Google-account: *Your email must be verified*
2. Using your Facebook-account: *Your Tinder must be connected to your Facebook*
3. Using your phone number: *This will require you to manually enter your received code*

### Login by Google & Facebook (RECOMMENDED)
```
session.login_using_google(email, password)
session.login_using_facebook(email, password)
```
**Required parameters**</br>
`email`: *string*</br>
`password`: *string*</br>

**Example usage**</br>
```
session.login_using_google("myemail@gmail.com", "password123")
session.login_using_facebook("myemail@gmail.com", "password123")
```

### Login by SMS (DEPRECATED)
```
session.login_using_sms(country, phone_number)
```
**Required parameters**</br>
`country`: *string*</br>
`phone_number`: *string*</br>

**Example usage**</br>
Let's say your phone_number is +32401234567, then </br>
***country*** is needed to get the right prefix, in my case +32 and</br>
***phone_number*** is everything after the prefix (+32).</br>
```
session.login_using_sms("Belgium", "401234567")
```
**NOTE**: this is not my phone number :)</br>


# Settings
## Custom Location
Changing location used to be a paid for ***Tinder Plus*** feature. But no more!</br>
We are now able to mask our position using geopositioning inside our browser.</br>
```
session.set_custom_location(latitude, longitude)
```
**Required parameters**</br>
`latitude`: *float*</br>
`longitude`: *float*</br>

**Optional parameters**</br>
`accuracy`: *string*</br>

***Note:*** By default, accuracy is 100%, which is recommended.</br>

**Example usage**</br>
In this example we set the location to the city Leuven in Belgium.</br>
You can find the latitude and longitude of a location online; for example [here](https://www.latlong.net).<br>
```
session.set_custom_location(latitude=50.879829, longitude=4.700540, accuracy="100%")
# would be the same as simply
session.set_custom_location(latitude=50.879829, longitude=4.700540)
```

## Email Notifications
You can activate the option to receive an email whenever you get a match. The email, which you've used to login with, is being used as recepient.
By default no emails are being sent. If you wish to receive emails you need to set this setting to **True**.
```
session.set_email_notifications(boolean)
```

**Required parameters**</br>
`boolean`: *boolean*</br>

**Example usage**</br>
```
session.set_email_notifications(True)
```

## Distance Range
The distance range function allows you to set the maximum allowed distance to your potential matches.</br>
This setting requires you to be logged in on Tinder.</br>
Note: the parameter passed is the distance to you in ***kilometers***.
```
session.set_distance_range(km)
```
**Required parameters**</br>
`km`: *integer*</br>

**Example usage**</br>
```
session.set_distance_range(150)
```

## Age Range
First parameter is the minimum age, second parameter is the maximum age of the potential matches.</br>
This setting requires you to be logged in on Tinder.</br>
```
session.set_age_range(min, max)
```
**Required parameters**</br>
`min`: *integer*</br>
`max`: *integer*</br>

**Example usage**</br>
```
session.set_age_range(18, 25)
```

## Sexuality
[Click here](https://github.com/frederikme/TinderBotz/blob/master/tinderbotz/helpers/constants_helper.py) to see what sexualities are allowed by Tinder.</br>
This setting allows you to choose which gender you get to see and thus will be matched with.</br>
This setting requires you to be logged in on Tinder.</br>
```
from tinderbot.helpers.constants_helper import Sexuality
session.set_sexuality(type)
```
**Required parameters**</br>
`type`: *(enum) sexuality*</br>

**Example usage**</br>
```
session.set_sexuality(Sexuality.EVERYONE)
```

## Global
This setting allows you to match other people around the world.</br>
This setting requires you to be logged in on Tinder.</br>
```
session.set_global(boolean)
```
**Required parameters**</br>
`boolean`: *boolean*</br>

**Optional parameters**</br>
***Note: Currently this option is not available yet in this project. Please open an issue for feature request if you'd want this feature to be made available.***
`language`: [Click here](https://github.com/frederikme/TinderBotz/blob/master/tinderbotz/helpers/constants_helper.py) to see what global languages are available.</br>

**Example usage**</br>
```
session.set_global(True)
```

# Actions
## Liking Geomatches
Liking method has 4 optional parameters.</br>
The amount, which is by default equal to 1, specifies how many times the like button should be pressed.</br>
The ratio, which is by default 100%, is the chance the bot should press like or else dislike.</br>
The sleep, which is by default 0 seconds, is the amount of seconds the bot should sleep between likes.</br>
The randomize_sleep, which is by default True, if set to True, adds randomization to the provided time between likes.</br>

These last 3 should make sure you don't get banned. :)
```
session.like()
```
**Optional parameters**</br>
`amount`: *integer*</br>
`ratio`: *string*</br>
`sleep`: *integer*</br>

**Example usage**</br>
```
session.like(amount=10, ratio="72.5%", sleep=1)
```

## Disliking Geomatches
```
session.dislike()
```
**Optional parameters**</br>
`amount`: *integer*</br>

**Example usage**</br>
```
session.dislike(amount=25)
```

## Superliking Geomatches
```
session.superlike()
```
**Optional parameters**</br>
`amount`: *integer*</br>

**Example usage**</br>
```
session.superlike(amount=2)
```

## Getting Matches
Your matches can be placed into two categories:
1. New matches with whom you haven't exchanged messages with yet.
2. Messaged matches with whom you have already interacted.
These matches will be a list of objects of the [class Match](https://github.com/frederikme/TinderBotz/blob/master/tinderbotz/helpers/match.py) which is a childclass of the [class Geomatch](https://github.com/frederikme/TinderBotz/blob/master/tinderbotz/helpers/geomatch.py).
```
new_matches = session.get_new_matches()    
old_matches = session.get_messaged_matches()

# getting all matches can be done by adding both together
matches = new_matches + old_matches
```
**Optional parameters**</br>
`amount`: *amount*</br>
`quickload`: *boolean*</br>

**Example usage**</br>
```
new_matches = session.get_new_matches(amount=100, quickload=True)    
old_matches = session.get_messaged_matches(amount=15, quickload=False)
```
By default, all new and messaged matches are being loaded, although quite often it's more interesting to load only a handful matches. The amount of matches you want to fetch can be adjusted by specifying the amount of matches.</br>

**Note**: **quickload** is **True** by default when no parameter is passed. This makes sure the loading happens two times faster while still getting most of the information, but only ***a few images*** of the match are loaded. </br>
However when **quickload** is **False**, ***ALL images*** of the match are loaded.</br>

**Note**: When quickload is **False**, loading your matches might take a while depending on how many matches you have.</br>
This is because the session will iterate through every match and all their images one by one.</br>

Another option, besides quickloading, to reduce loading time is to store these matches at the first run as illustrated here: [Storing (geo)Matches](#storing-geomatches)</br>
and then load them from there in future runs.</br>

## Getting Geomatches
Get data *name, age, bio, distance, home, study, passions, images...* of the displayed geomatch and store it inside an object of the [class Geomatch()](https://github.com/frederikme/TinderBotz/blob/master/tinderbotz/helpers/geomatch.py).
```
geomatch = session.get_geomatch()
```
**Optional parameters**</br>
`quickload`: *boolean*</br>

**Note**: **quickload** is **True** by default when no parameter is passed. This makes sure the loading happens two times faster while still getting most of the information, but only ***a few images*** of the geomatch are loaded. </br>
However when **quickload** is **False**, ***ALL images*** of the geomatch are loaded.</br>

## Storing (geo)Matches
Every profile, also known as a (geo)match, can be stored locally. </br>
Storing data can be useful for reducing runtime, for example when needing to fetch your matches.</br>
```
matches = session.getAllMatches()
for match in matches:
   session.store_local(match)
   
geomatch = session.get_geomatch()
session.store_local(geomatch)
```
## Sending Messages
Messages can be sent to matches.</br>
[Scrape your matches](#getting-matches) or fetch them from your locally stored json file.</br>
 ```
id = match.get_chat_id()
name = match.get_name()
 
pickup_line = "Hey {}, you got look exactly like my future wife. ;)".format(name)

# send them a unique pick up line with their personal name
session.send_message(chatid=id, message=pickup_line)
```
## Sending GIFS
GIFS can be sent to matches.</br>
[Scrape your matches](#getting-matches) or get them from your locally stored json file.</br>
</br>
Sending a GIF will open the correct chat with your match, browse for the gif and send the first one that's being displayed.
```
id = match.get_chat_id()
session.send_gif(chatid=id, gifname="pizza")
```
## Sending Songs
Songs can be sent to matches.</br>
[Scrape your matches](#getting-matches) or get them from your locally stored json file.</br>
</br>
Sending a song will open the correct chat with your match, browse for the song and send the first one that's being displayed.
```
id = match.get_chat_id()
session.send_song(chatid=id, songname="cutiepie")
```
## Sending Socials
Socials can be sent to matches.</br>
[Scrape your matches](#getting-matches) or get them from your locally stored json file.</br>
</br>
There are different types of socials. [Click here](https://github.com/frederikme/TinderBotz/blob/master/tinderbotz/helpers/constants_helper.py) to see what types of social media or available.</br> 
```
id = match.get_chat_id()
session.send_socials(chatid=id, media=Socials.INSTAGRAM, value="Teeti.fm")
```
## Unmatching
You can unmatch a match. **BUT** think twice before you do. Once you unmatch, there is no going back.
```
id = match.get_chat_id()
session.unmatch(chatid=id)
```

# ***JUST LET ME START ALREADY YES PLS TY***
If you feel like you just want to dive right into the code and get started right away, this is where you need to be. :) </br>

1. Open the [quickstart.py](https://github.com/frederikme/TinderBotz/blob/master/quickstart.py) from the tinderbot directory.
2. Fill in your credentials (email and password) to be able to login to Tinder.
3. Change the quickstart script to your needs.
4. Run the code.

If you want to scrape as much *geomatches* as possible,</br>
then [scraper.py](https://github.com/frederikme/TinderBotz/blob/master/scraper.py) will suit your needs better.
