from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import pyfiglet
import os
import time

from helpers.geomatch import Geomatch
from helpers.login_helper import LoginHelper
from helpers.geomatch_helper import GeomatchHelper
from helpers.match_helper import MatchHelper


class TinderBot:

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

    def loginUsingFacebook(self, email, password):
        if not self.isLoggedIn():
            helper = LoginHelper(browser=self.browser)
            helper.loginByFacebook(email, password)

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

    def getGeomatch(self, latitude=None, longitude=None):
        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)

            name = helper.getName()
            age = helper.getAge()
            distance = helper.getDistance()
            bio = helper.getBio()
            image_urls = helper.getImageURLS()

            return Geomatch(name=name, age=age, distance=distance, bio=bio, image_urls=image_urls,
                            lat_scraper=latitude, long_scraper=longitude)

    def getAllMatches(self):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            return helper.getAllMatches()

    def getNewMatches(self):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            return helper.getNewMatches()

    def getMessagedMatches(self):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            return helper.getMessagedMatches()

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

    def refresh(self):
        print("Refreshing url: {}".format(self.browser.current_url))
        self.browser.get(self.browser.current_url)

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
