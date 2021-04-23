'''
Created by Frederikme (TeetiFM)
'''
import random, time
from tinderbotz.session import Session

if __name__ == "__main__":

    # creates instance of session
    session = Session()

    # set a custom location
    session.set_custom_location(latitude=50.879829, longitude=4.700540)
    
    # replace this with your own email and password!
    email = "example@gmail.com"
    password = "password123"
    
    # login using your google account with a verified email! Alternatively, you can use Facebook login
    session.login_using_facebook(email, password)

    # start scraping as much geomatches as possible
    while True:
        # When scraping we want ALL images and not just the first few.
        # If you want to scrape a lot quicker, I recommend putting quickload on True
        # But note that you'd only get 1-3 image urls instead of them all.
        geomatch = session.get_geomatch(quickload=False)

        # check if crucial data is not empty (This will rarely be the case tho, but we want a 'clean' dataset
        if geomatch.get_name() is not None \
                and geomatch.get_image_urls() != []:

            # let's store the data of the geomatch locally (this includes all images!)
            session.store_local(geomatch)

            # display the saved data on your console
            print(geomatch.get_dictionary())

            # account is scraped, now dislike and go next (since dislikes are infinite)
            # NOTE: if no amount is passed, it will dislike once -> same as => dislike(amount=1)
            # NOTE: if you have TinderPlus, -Gold or -Platinum you could also use session.like()
            session.dislike()

        else:
            # refresh webpage, and go for another geomatch
            session.browser.refresh()

        # make a random sleep between dislikes between 0 and 4 seconds to mimic looks human-like, not spammy behaviour
        sleepy_time = random.random() * 4
        time.sleep(sleepy_time)

