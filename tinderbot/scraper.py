'''
Created by Frederikme (TeetiFM)
Examples of usage are demonstrated in this quickstart.py file
'''
import random, time
from bot import TinderBot
import constants


email = constants.email_facebook
password = constants.password_facebook

latitude = constants.lat_kam
longitude = constants.lon_kam

if __name__ == "__main__":

    # creates instance of bot
    bot = TinderBot()

    # login using your google account
    #bot.loginUsingGoogle(email=email, password=password)
    bot.loginUsingFacebook(email=email, password=password)


    # start scraping as much geomatches as possible
    #while True:
    for _ in range(2):
        # get user
        geomatch = bot.getGeomatch(latitude=latitude, longitude=longitude)

        # check if crucial data is not being skipped
        if geomatch.getName() is not None \
                and geomatch.getImageURLS() != []:

            # let's store the data of the geomatch locally
            geomatch.storeLocal()

            # display data in terminal
            print(geomatch.getDictionary())

            # account is scraped, now dislike and go next (since dislikes are infinite)
            bot.dislike(amount=1)

        else:
            # refresh webpage, and go for another geomatch
            bot.refresh()

        # make a random sleep between dislikes between 0 and 4 seconds so it looks human-like behaviour
        sleepy_time = random.random() * 4
        time.sleep(sleepy_time)

