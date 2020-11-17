'''
Created by Frederikme (TeetiFM)
'''
import random, time
from tinderbot.session import Session
import constants

if __name__ == "__main__":

    # creates instance of session
    session = Session()

    # set a custom location
    session.setCustomLocation("Leuven, Belgium")

    # login using your google account with a verified email!
    session.loginUsingGoogle(email=constants.email_google, password=constants.password_google)

    # Alternatively you can login using facebook with a connected profile!
    session.loginUsingFacebook(email=constants.email_facebook, password=constants.password_facebook)

    # start scraping as much geomatches as possible
    while True:
        # get user
        geomatch = session.getGeomatch()

        # check if crucial data is not empty (This will rarely be the case tho, but we want a 'clean' dataset
        if geomatch.getName() is not None \
                and geomatch.getImageURLS() != []:

            # let's store the data of the geomatch locally
            session.storeLocal(geomatch)

            # display the saved data in terminal
            print(geomatch.getDictionary())

            # account is scraped, now dislike and go next (since dislikes are infinite)
            # NOTE: if no amount is passed, it will dislike once -> same as => dislike(amount=1)
            session.dislike()

        else:
            # refresh webpage, and go for another geomatch
            session.refresh()

        # make a random sleep between dislikes between 0 and 4 seconds so it looks human-like behaviour
        sleepy_time = random.random() * 4
        time.sleep(sleepy_time)

