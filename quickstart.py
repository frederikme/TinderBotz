'''
Created by Frederikme (TeetiFM)
'''

from tinderbotz.session import Session
from tinderbotz.helpers.constants_helper import *

if __name__ == "__main__":
    # creates instance of session
    session = Session()

    # set location (Don't need to be logged in for this)
    session.setCustomLocation("Leuven, Belgium")
    
    # replace this with your own email and password!
    email = "example@gmail.com"
    password = "password123"
    
    # login using your google account with a verified email!
    session.loginUsingGoogle(email, password)

    # Alternatively you can login using facebook with a connected profile!
    session.loginUsingFacebook(email, password)

    # Alternatively, you can also use your phone number to login
    '''
    - country is needed to get the right prefix, in my case +32
    - phone_number is everything after the prefix (+32)
    NOTE: this is not my phone number :)
    '''
    country = "Belgium"
    phone_number = "479011124"
    session.loginUsingSMS(country, phone_number)

    # spam likes, dislikes and superlikes
    # to avoid being banned:
    #   - it's best to apply a randomness in your liking by sometimes disliking.
    #   - some sleeping between two actions is recommended
    # NOTE: these recommendations apply mostly to large amounts of swiping (+100 likes)
    session.like(amount=10, ratio="72.5%", sleep=1)
    session.dislike(amount=1)
    session.superlike(amount=1)
    
    # adjust allowed distance for geomatches
    # Note: You need to be logged in for this setting
    # Note: PARAMETER IS IN KILOMETERS!
    session.setDistanceRange(km=150)

    # set range of allowed ages
    # Note: You need to be logged in for this setting
    session.setAgeRange(18, 55)

    # set interested in gender(s) -> options are: WOMEN, MEN, EVERYONE
    session.setSexuality(Sexuality.WOMEN)

    # Allow profiles from all over the world to appear
    session.setGlobal(True)

    # Getting matches takes a while, so recommended you load as much as possible from local storage
    # get new matches, with whom you haven't interacted yet
    # Let's load the first 10 new matches to interact with later on.
    new_matches = session.getNewMatches(amount=10)
    # get already interacted with matches (matches with whom you've chatted already)
    messaged_matches = session.getMessagedMatches()
    
    # you can store the data and images of these matches now locally in data/matches
    # For now let's just store the messaged_matches
    for match in messaged_matches:
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
        session.sendSocials(chatid=id, media=Socials.INSTAGRAM, value="Fredjemees")

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
