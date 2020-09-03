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
## Make your adjustments in the template.py file
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

# this will return you your matches as objects of helperclass Match
matches = bot.getMatches()
# you can easily iterate through your matches by using a for loop
for match in matches:
    print(match.getName(), match.getID())
```
