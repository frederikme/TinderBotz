from bot import *

email = "example@email.com"
password = "password123"

if __name__ == "__main__":

    # creates instance of bot
    bot = TinderBot()

    # login using your verified email / google account
    bot.loginUsingGoogle(email=email, password=password)

    # spam likes
    bot.like(amount=50)

    # get new, not yet interacted with, matches
    matches = bot.getNewMatches()

    # create pick up line with place to insert name to make it more personal
    pick_up_line = "Hey {}, you look good!"

    # iterate through these matches
    for match in matches:

        name = match.getName()
        id = match.getID()

        # insert the name into the pick up line
        message = pick_up_line.format(name)

        # send message
        bot.sendMessage(id=id, message=message)

