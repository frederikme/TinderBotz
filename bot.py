from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import pyfiglet
import os
import time

from helpers.geomatch import Geomatch
from helpers.login_helper import LoginHelper
from helpers.geomatch_helper import GeomatchHelper
from helpers.match_helper import MatchHelper
from helpers.socials import Socials

class TinderBot:

    delay = 5
    HOME_URL = "https://www.tinder.com/app/recs"

    def __init__(self):
        # clear the console and show some basic info
        os.system("clear")
        text = "Tinderbot"
        print(pyfiglet.figlet_format(text))
        print("-> Made by Frederikme")
        print("-----------------------------------\n\n")

        # getting chromedriver from cache or download from internet
        print("Getting ChromeDriver ...")
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
    
    def loginUsingGoogle(self, email, password):
        if not self.isLoggedIn():
            helper = LoginHelper(browser=self.browser)
            helper.loginByGoogle(email, password)

    def like(self, amount=1):
        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)
            helper.like(amount)

    def dislike(self, amount=1):
        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)
            helper.dislike(amount)

    def superlike(self, amount=1):
        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)
            helper.superlike(amount)

    def getGeomatch(self):
        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)

            name = helper.getName()
            age = helper.getAge()
            distance = helper.getDistance()
            bio = helper.getBio()
            image_urls = helper.getImageURLS()

            return Geomatch(name=name, age=age, distance=distance, bio=bio, image_urls=image_urls)

    def getAllMatches(self):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            return helper.getAllMatches()

    def getNewMatches(self):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            return helper.getNewMatches()

    def getChattedMatches(self):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            return helper.getChattedMatches()

    def sendMessage(self, chatid, message):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            return helper.sendMessage(chatid, message)

    def sendGif(self, chatid, gifname):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            return helper.sendGif(chatid, gifname)

    def sendSong(self, chatid, songname):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            return helper.sendSong(chatid, songname)

    def sendSocials(self, chatid, media, value):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            return helper.sendSocials(chatid, media, value)

    def unMatch(self, chatid):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            return helper.unMatch(chatid)

    def isLoggedIn(self):
        # make sure tinder website is loaded for the first time
        if not "tinder" in self.browser.current_url:
            self.browser.get(self.HOME_URL)
            time.sleep(1.5)

        if "tinder.com/app/" in self.browser.current_url:
            return True
        else:
            print("User is not logged in yet.")
            return False
