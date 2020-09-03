'''
Created by Frederikme (TeetiFM)
Examples of usage are demonstrated in this template.py file
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

    # spam likes
    bot.like(amount=0)
    # spam dislikes
    bot.dislike(amount=0)
    # spam superlikes
    bot.superlike(amount=0)

    # There are 2 types of matches:
    #  - new matches with whom you haven't interacted yet
    bot.getNewMatches()
    #  - matches with whom you've already chatted
    bot.getChattedMatches()
    # - or simply get all matches (new+chatted)
    matches = bot.getAllMatches()

    # Potentially iterate through these matches
    for match in matches:
        print(match.getName(), match.getID())

    # opening a chat can be done by 3 different parameters
    bot.openChat(match=matches[0])
    bot.openChat(id=matches[1].getID())
    bot.openChat(mref=matches[2].getMRef())
