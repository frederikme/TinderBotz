# TinderBot
Simple bot for Tinder using selenium written in python3

## Make sure python and pip are installed
Pip should be included with python by default.<br />
Dowload python: https://www.python.org/downloads/

## Usage of a virtual environment recommended
### install virtualenv
```
pip3 install virtualenv 
```
### Create virtual environment
```
virtualenv venv
```
### Activate virtual environment
```
source venv/bin/activate
```
### To deactivate or leave the virtual environment
```
deactivate
```
## Install dependencies (preferably in the venv)
```
pip3 install -r requirements.txt
```
## Features
```
# create instance of the bot
bot = TinderBot()

# you need a verified email to login like this
bot.loginUsingGoogle(email, password) 

# alternatively you can login using Facebook
bot.loginUsingFacebook(email, password)

# this will (dis/super)like x amount of people in a row -> is spammable if you higher the amount
bot.like(amount=10) 
bot.dislike(amount=3)
bot.superlike(amount=1)

# There are 2 types of matches:
#  - new matches with whom you haven't interacted yet
#  - matches with whom you've already chatted/interacted
new_matches = bot.getNewMatches()
messaged_matches = bot.getChattedMatches()

# - or simply get all matches (new+chatted) by default store_local=True stored in /data/matches.json
matches = bot.getAllMatches(store_local=False)

# send chats to a user
bot.sendMessage(toID=matches[0].getID(), message="hey")

# returns a url to the image of the match (AND when by default store_local=True it will store the image as jpeg in /data/images/matchid.jpg
bot.getImage(matches[0].getID(), store_local=False)

# searches for a gif and then sends the first one of the query
bot.sendGif(id, gifname)

# searches for a song and then sends the first one of the query
bot.sendSong(id, songname)

# send my Socials.INSTAGRAM or you can use alternative socials like facebook, phonenumber and snapchat and value as username
bot.sendSocials(id, media, value)

# possibilty to unmatch your match by id
bot.unMatch(id)
```
