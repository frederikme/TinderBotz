'''
Created by Frederikme (TeetiFM)
Examples of usage are demonstrated in this quickstart_analytics.py file
'''

from tinderbot.session import Session
from tinderbot.helpers.socials import Socials

import constants

if __name__ == "__main__":

    # creates instance of session
    session = Session()

    # login using your google account with a verified email!
    # session.loginUsingGoogle(email=constants.email_google, password=constants.password_google)

    # Alternatively you can login using facebook with a connected profile!
    session.loginUsingFacebook(email=constants.email_facebook, password=constants.password_facebook)

    '''
    Recommended to fill in using your location from where you're scraping 
        - Peoples exact location can be calculated after multiple scrapes from different locations
            -> An intersection will be made from the circles/distance of your location to the profile over multiple scrapes
    '''
    session.setScrapersLocation(latitude=constants.lat_kort, longitude=constants.lon_kort)

    # spam likes, dislikes and superlikes
    session.like(amount=10)
    session.dislike(amount=1)
    session.superlike(amount=1)

    # Getting matches takes a while, so recommended you load as much as possible from local storage
    # get new matches, with whom you haven't interacted yet
    new_matches = session.getNewMatches()
    # get already interacted with matches
    old_matches = session.getMessagedMatches()
    # get all matches (comment out new_matches and old_matches above so it doesnt load it all for no reason)
    matches = session.getAllMatches()

    # you can store the data and images of these matches now locally in data/matches
    for match in matches:
        session.storeLocal(match)

    # Pick up line with their personal name so it doesn't look spammy
    pickup_line = "Hey {}! You. Me. Pizza? Or do you not like pizza?"

    # loop through my new matches and send them the first message of the conversation
    for match in new_matches:
        # store name and chatid in variables so we can use it more simply later on
        name = match.getName()
        id = match.getChatID()

        # Format the match her/his name in your pickup line for a more personal approach.
        message = pickup_line.format(name)

        # send pick up line with their name in it to all my matches
        session.sendMessage(chatid=id, message=message)

        # send a funny gif
        session.sendGif(chatid=id, gifname="pizza")

        # send a funny song
        session.sendSong(chatid=id, songname="cutiepie")

        # send my instagram or you can use alternative socials like facebook, phonenumber and snapchat
        session.sendSocials(chatid=id, media=Socials.INSTAGRAM, value="Teeti.fm")

        # you can also unmatch
        session.unMatch(chatid=id)

    # let's scrape some geomatches now
    for _ in range(50):
        # get profile data (name, age, bio, images, ...)
        geomatch = session.getGeomatch()
        # store this data locally as json with reference to their respective (locally stored) images
        session.storeLocal(geomatch)
        # dislike the profile, so it will show us the next geomatch (since we got infinite amount of dislikes anyway)
        session.dislike(1)
