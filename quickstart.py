'''
Created by Frederikme (TeetiFM)
'''

from tinderbot.session import Session
from tinderbot.helpers.constants_helper import Socials, Sexuality

import constants

if __name__ == "__main__":

    # creates instance of session
    session = Session()

    # set location (Don't need to be logged in for this)
    session.setCustomLocation("Leuven, Belgium")

    # login using your google account with a verified email!
    session.loginUsingGoogle(email=constants.email_google, password=constants.password_google)

    # Alternatively you can login using facebook with a connected profile!
    session.loginUsingFacebook(email=constants.email_facebook, password=constants.password_facebook)

    # adjust allowed distance for geomatches
    # Note: You need to be logged in for this setting
    # Note: PARAMETER IS IN KILOMETERS!
    session.setDistanceRange(km=150)

    # set range of allowed ages
    # Note: You need to be logged in for this setting
    session.setAgeRange(25, 44)

    # set interested in gender(s) -> options are: WOMEN, MEN, EVERYONE
    session.setSexuality(Sexuality.WOMEN)

    # Allow profiles from all over the world to appear
    session.setGlobal(True)

    # spam likes, dislikes and superlikes
    session.like(amount=1)
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

        print(name, id)

        # Format the match her/his name in your pickup line for a more personal approach.
        message = pickup_line.format(name)

        # send pick up line with their name in it to all my matches
        session.sendMessage(chatid=id, message=message)

        # send a funny gif
        session.sendGif(chatid=id, gifname="")

        # send a funny song
        session.sendSong(chatid=id, songname="")

        # send my instagram or you can use alternative socials like facebook, phonenumber and snapchat
        session.sendSocials(chatid=id, media=Socials.INSTAGRAM, value="Teeti.fm")

        # you can also unmatch
        #session.unMatch(chatid=id)

    # let's scrape some geomatches now
    for _ in range(5):
        # get profile data (name, age, bio, images, ...)
        geomatch = session.getGeomatch()
        # store this data locally as json with reference to their respective (locally stored) images
        session.storeLocal(geomatch)
        # dislike the profile, so it will show us the next geomatch (since we got infinite amount of dislikes anyway)
        session.dislike()
