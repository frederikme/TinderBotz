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
#### Create instance of the bot
```
bot = TinderBot()
```
#### You need a verified email to login like this, alternatively you can login using Facebook.
```
bot.loginUsingGoogle(email, password) 
bot.loginUsingFacebook(email, password)
```
#### You can (dis/super)like x amount of people in a row.
```
bot.like(amount) 
bot.dislike(amount)
bot.superlike(amount)
```
#### Getting your matches.
  - new matches with whom you haven't interacted yet</br>
  - matches with whom you've already chatted/interacted</br>
  - or simply get all matches (AND when by default store_local=True it will store all match data in /data/matches.json
```
new_matches = bot.getNewMatches()
messaged_matches = bot.getChattedMatches()
matches = bot.getAllMatches()
```
#### Sending a  message to match.
```
bot.sendMessage(id, message)
```
#### Return url to image of the match (AND when by default store_local=True it will store the image as jpeg in /data/images/matchid.jpg)
```
image_url = bot.getImage(id)
```
#### Searches for a gif/song and then sends the first one of the query to a match.
```
bot.sendGif(id, gifname)
bot.sendSong(id, songname)
```
#### Sending my Socials.INSTAGRAM or you can use alternative socials like facebook, phonenumber and snapchat and value as username.
```
bot.sendSocials(id=id, media=Socials.INSTAGRAM, value="myinstagramaccount")
```
#### Unmatch your match.
```
bot.unMatch(id)
```
