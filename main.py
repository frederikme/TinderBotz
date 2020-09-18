
from bot import *
from helpers.socials import Socials
import constants

email = constants.email
password = constants.password

if __name__ == "__main__":

    # creates instance of bot
    bot = TinderBot()

    # login using your google account
    bot.loginUsingGoogle(email=email, password=password)

    # alternatively login using facebook (might need adjustments and follow up, so if you feel like contributing ;)
    bot.loginUsingFacebook(email=email, password=password)

    # spam likes, dislikes and superlikes
    bot.like(amount=5)
    bot.dislike(amount=0)
    bot.superlike(amount=0)

    # get new matches, with whom you haven't interacted yet
    new_matches = bot.getNewMatches()
    # get already interacted with matches
    old_matches = bot.getChattedMatches()
    # get all matches and store them also locally in data directory
    matches = bot.getAllMatches(store_local=True)

    # My pick up line with personal name so it doesn't look spammy
    pickup_line = "Hey {}! You. Me. Pizza? Or do you not like pizza?"

    # loop through my new matches
    for match in new_matches:
        # store name and id locally so we can use it more simply
        name = match.getName()
        id = match.getID()

        # start by storing their image and storing them in our data directory
        bot.getImage(id=id, store_local=True)

        # send pick up line with their name in it to all my matches
        bot.sendMessage(id=id, message=pickup_line.format(name))

        # send a funny gif
        bot.sendGif(id=id, gifname="pizza")

        # send a funny song
        bot.sendSong(id=id, songname="cutiepie")

        # send my instagram or you can use alternative socials like facebook, phonenumber and snapchat
        bot.sendSocials(id=id, media=Socials.INSTAGRAM, value="Teeti.fm")

        # you can also unmatch
        # bot.unMatch(id=id)