# TinderBot
Simple bot for Tinder using selenium written in python3

## Make sure python and pip are installed
Pip should be included with python by default.<br/>
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
## Usage
Create instance of the bot
```
bot = TinderBot()
```
You need a verified email to login like this
```
bot.loginUsingGoogle(email, password) 
# alternatively you can login using Facebook
bot.loginUsingFacebook(email, password)
```
You can (dis/super)like x amount of people in a row
```
bot.like(amount) 
bot.dislike(amount)
bot.superlike(amount)
```
There are 2 types of matches:<br/>
- new matches with whom you haven't interacted yet</br>
- matches with whom you've already chatted/interacted
```
new_matches = bot.getNewMatches()
messaged_matches = bot.getChattedMatches()
# or simply get all matches (new+chatted)
matches = bot.getAllMatches()
```
Sending a  message to a user
```
bot.sendMessage(id, message)
```
Return url to image of the match (AND when by default store_local=True it will store the image as jpeg in /data/images/matchid.jpg
```
bot.getImage(id)
```
# searches for a gif and then sends the first one of the query
bot.sendGif(id, gifname)

# searches for a song and then sends the first one of the query
bot.sendSong(id, songname)

# send my Socials.INSTAGRAM or you can use alternative socials like facebook, phonenumber and snapchat and value as username
bot.sendSocials(id, media, value)

# possibilty to unmatch your match by id
bot.unMatch(id)
```
