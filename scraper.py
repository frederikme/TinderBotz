'''
Created by Frederikme (TeetiFM)
Examples of usage are demonstrated in this quickstart_analytics.py file
'''
import random, time
from tinderbot.session import Session
import constants

if __name__ == "__main__":

    # creates instance of session
    session = Session()

    # login using your google or facebook account
    # session.loginUsingGoogle(email=constants.email_google, password=constants.password_google)
    session.loginUsingFacebook(email=constants.email_facebook, password=constants.password_facebook)

    # Setting location of scraper is recommended, but not necessary
    session.setScrapersLocation(latitude=constants.lat_kort, longitude=constants.lon_kort)

    # start scraping as much geomatches as possible
    while True:
        # get user
        geomatch = session.getGeomatch()

        # check if crucial data is not being skipped
        if geomatch.getName() is not None \
                and geomatch.getImageURLS() != []:

            # let's store the data of the geomatch locally
            session.storeLocal(geomatch)

            # display the saved data in terminal
            print(geomatch.getDictionary())

            # account is scraped, now dislike and go next (since dislikes are infinite)
            # by default dislike(amount=1)
            session.dislike()

        else:
            # refresh webpage, and go for another geomatch
            session.refresh()

        # make a random sleep between dislikes between 0 and 4 seconds so it looks human-like behaviour
        sleepy_time = random.random() * 4
        time.sleep(sleepy_time)

