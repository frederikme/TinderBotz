'''
Created by Frederikme (TeetiFM)

This script is meant to be user friendly for beginning users.
Simply replace email and password with your private information.
'''

from tinderbotz.session import Session
from tinderbotz.helpers.constants_helper import *

if __name__ == "__main__":

    # creates instance of session
    session = Session()
    
    # replace this with your own email and password!
    email = "example@gmail.com"
    password = "password123"
    
    # login using your google account with a verified email! You can also log in using Facebook.
    session.loginUsingGoogle(email, password)
    
    # spam likes
    # amount -> amount of people you want to like
    # ratio  -> chance of liking/disliking
    # sleep  -> amount of seconds to wait before swiping again
    session.like(amount=100, ratio="72.5%", sleep=1)
