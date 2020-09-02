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

    # login
    bot.loginUsingGoogle(email=email, password=password)

    bot.getMatches()

    '''
    # spam likes
    bot.like(amount=3)
    # spam dislikes
    bot.dislike(amount=1)
    # spam superlikes
    bot.superlike(amount=2)
    '''