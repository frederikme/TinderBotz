'''
Created by Frederikme (TeetiFM)
Examples of usage are demonstrated in this quickstart_analytics.py file
'''

from tinderbot.bot import TinderBot
from tinderbot.helpers.socials import Socials
'''
Login credentials
    google   -> Make sure your email is verified
    facebook -> Make sure your tinder profile is linked with you Facebook account
'''
email = "myemail@gmail.com"
password = "mypassword"

'''
Recommended to fill in using your location from where you're scraping 
    - Peoples exact location can be calculated after multiple scrapes from different locations
    - An intersection will be made from the circles (distance) of your location to the profile over multiple scrapes
'''
latitude = None
longitude = None

if __name__ == "__main__":

    # creates instance of bot
    bot = TinderBot()

    # login using your google account with a verified email!
    bot.loginUsingGoogle(email=email, password=password)

    # Alternatively you can login using facebook
    bot.loginUsingFacebook(email=email, password=password)

    # spam likes, dislikes and superlikes
    bot.like(amount=5)
    bot.dislike(amount=0)
    bot.superlike(amount=0)

    # Getting matches takes ages, when you have a lot of matches: This needs a fix + local storage and reloading
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

        # store name and chatid in variables so we can use it more simply later on
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
    for _ in range(50):
        # get profile data (name, age, bio, images, ...)
        geomatch = bot.getGeomatch(latitude=latitude, longitude=longitude)
        # store this data locally as json with reference to their respective (locally stored) images
        geomatch.storeLocal()
        # dislike the profile, so it will show us the next geomatch (since we got infinite amount of dislikes anyway)
        bot.dislike(1)
