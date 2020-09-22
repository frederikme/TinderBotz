'''
Created by Frederikme (TeetiFM)
Examples of usage are demonstrated in this quickstart.py file
'''

from bot import TinderBot
from helpers.socials import Socials

email = "example@email.com"
password = "password123"

if __name__ == "__main__":

    # creates instance of bot
    bot = TinderBot()

    # login using your google account with a verified email!
    bot.loginUsingGoogle(email=email, password=password)

    # spam likes, dislikes and superlikes
    bot.like(amount=5)
    bot.dislike(amount=0)
    bot.superlike(amount=0)

    # get new matches, with whom you haven't interacted yet
    new_matches = bot.getNewMatches()
    # get already interacted with matches
    old_matches = bot.getMessagedMatches()
    # get all matches
    matches = bot.getAllMatches()

    # you can store the data and images of these matches now locally in data/matches
    for match in matches:
        match.storeLocal()

    # Pick up line with their personal name so it doesn't look spammy
    pickup_line = "Hey {}! You. Me. Pizza? Or do you not like pizza?"

    # loop through my new matches and send them the first message of the conversation
    for match in new_matches:

        # store name and chatid in variable so we can use it more simply
        name = match.getName()
        id = match.getChatID()

        # send pick up line with their name in it to all my matches
        bot.sendMessage(chatid=id, message=pickup_line.format(name))

        # send a funny gif
        bot.sendGif(chatid=id, gifname="pizza")

        # send a funny song
        bot.sendSong(chatid=id, songname="cutiepie")

        # send my instagram or you can use alternative socials like facebook, phonenumber and snapchat
        bot.sendSocials(chatid=id, media=Socials.INSTAGRAM, value="Teeti.fm")

        # you can also unmatch
        # bot.unMatch(chatid=id)

    # let's scrape some geomatches now
    for _ in range(10):
        # get profile data (name, age, bio, images, ...)
        geomatch = bot.getGeomatch()
        # store this data locally as json and reference to images
        # geomatch.storeLocal()
        # dislike the profile, so it will show us the next geomatch
        bot.dislike(1)
