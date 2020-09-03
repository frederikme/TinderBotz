'''
Created by Frederikme (TeetiFM)
examples of usage

/* Create instance/object */
bot = TinderBot()

/* Log in to Tinder by using your verified email of google */
bot.logingoogle(email="example@mail.com", password="password123")

'''

from bot import *

import constants

email = constants.email
password = constants.password

if __name__ == "__main__":

    # creates instance of bot
    bot = TinderBot()

    # login using your google account
    bot.loginUsingGoogle(email=email, password=password)

    # alternatively you can use
    bot.loginUsingFacebook(email=email, password=password)

    # There are 2 types of matches:
    #  - new matches with whom you haven't interacted yet
    #bot.getNewMatches()
    #  - matches with whom you've already chatted
    #bot.getChattedMatches()
    # - or simply get all matches (new+chatted)
    matches = bot.getAllMatches()

    # Potentially iterate through these matches
    for match in matches:
        print(match.getName(), match.getID())

    # spam likes
    bot.like(amount=0)
    # spam dislikes
    bot.dislike(amount=0)
    # spam superlikes
    bot.superlike(amount=0)
