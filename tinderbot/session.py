from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import pyfiglet
import os
import time

from tinderbot.helpers.geomatch import Geomatch
from tinderbot.helpers.match import Match
from tinderbot.helpers.geomatch_helper import GeomatchHelper
from tinderbot.helpers.match_helper import MatchHelper
from tinderbot.helpers.login_helper import LoginHelper
from tinderbot.helpers.storage_helper import StorageHelper
from tinderbot.helpers.loadingbar import LoadingBar


class Session:

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

        # initialize settings of session
        self.latitude = None
        self.longitude = None

    # Settings of the Session
    def setScrapersLocation(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    # Actions of the session
    def loginUsingGoogle(self, email, password):
        if not self.isLoggedIn():
            helper = LoginHelper(browser=self.browser)
            helper.loginByGoogle(email, password)

    def loginUsingFacebook(self, email, password):
        if not self.isLoggedIn():
            helper = LoginHelper(browser=self.browser)
            helper.loginByFacebook(email, password)

    def storeLocal(self, match):
        if isinstance(match, Match):
            filename = 'matches'
        elif isinstance(match, Geomatch):
            filename = 'geomatches'
        else:
            print("type of match is unknown, storing local impossible")
            print("Crashing in 3.2.1... :)")
            assert False

        # store its images
        for url in match.image_urls:
            hashed_image = StorageHelper.storeImageAs(url=url, directory='data/{}/images'.format(filename))
            match.images_by_hashes.append(hashed_image)

        # store its userdata
        StorageHelper.storeMatch(match=match, directory='data/{}'.format(filename), filename=filename)

    def like(self, amount=1):
        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)
            loadingbar = LoadingBar(amount, "likes")
            for index in range(amount):
                self.handlePotentialPopups()
                helper.like()
                loadingbar.updateLoadingBar(index)

    def dislike(self, amount=1):
        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)
            loadingbar = LoadingBar(amount, "dislikes")
            for index in range(amount):
                self.handlePotentialPopups()
                helper.dislike()
                loadingbar.updateLoadingBar(index)

    def superlike(self, amount=1):
        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)
            loadingbar = LoadingBar(amount, "dislikes")
            for index in range(amount):
                self.handlePotentialPopups()
                helper.superlike()
                loadingbar.updateLoadingBar(index)

    def getGeomatch(self):
        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)
            self.handlePotentialPopups()

            name = helper.getName()
            age = helper.getAge()
            distance = helper.getDistance()
            bio = helper.getBio()
            image_urls = helper.getImageURLS()

            return Geomatch(name=name, age=age, distance=distance, bio=bio, image_urls=image_urls,
                            lat_scraper=self.latitude, long_scraper=self.longitude)

    def getAllMatches(self):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            return helper.getAllMatches(lat_scraper=self.latitude, long_scraper=self.longitude)

    def getNewMatches(self):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            return helper.getNewMatches(lat_scraper=self.latitude, long_scraper=self.longitude)

    def getMessagedMatches(self):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            return helper.getMessagedMatches(lat_scraper=self.latitude, long_scraper=self.longitude)

    def sendMessage(self, chatid, message):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            return helper.sendMessage(chatid, message)

    def sendGif(self, chatid, gifname):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            return helper.sendGif(chatid, gifname)

    def sendSong(self, chatid, songname):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            return helper.sendSong(chatid, songname)

    def sendSocials(self, chatid, media, value):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            return helper.sendSocials(chatid, media, value)

    def unMatch(self, chatid):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            return helper.unMatch(chatid)

    # Utilities
    def handlePotentialPopups(self):
        delay = 2

        # try to deny see who liked you
        try:
            xpath = '//*[@id="modal-manager"]/div/div/div/div[3]/button[2]'
            WebDriverWait(self.browser, delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))

            denyBtn = self.browser.find_element_by_xpath(xpath)
            denyBtn.click()
            return "POPUP: Denied see who liked you"

        except NoSuchElementException:
            pass
        except TimeoutException:
            pass

        # try to deny 'add tinder to homescreen'
        try:
            xpath = '//*[@id="modal-manager"]/div/div/div[2]/button[2]'

            add_to_home_popup = self.browser.find_element_by_xpath(xpath)
            add_to_home_popup.click()
            return "POPUP: Denied Tinder to homescreen"

        except NoSuchElementException:
            pass

        # try to dismiss match
        try:
            xpath = '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/button'

            match_popup = self.browser.find_element_by_xpath(xpath)
            match_popup.click()
            return "POPUP: Dismissed NEW MATCH"

        except NoSuchElementException:
            pass

        # try to say 'no thanks' to buy more superlikes
        try:
            xpath = '//*[@id="modal-manager"]/div/div/div[3]/button[2]'
            denyBtn = self.browser.find_element_by_xpath(xpath)
            denyBtn.click()
            return "POPUP: Denied buying more superlikes"

        except NoSuchElementException:
            pass

        return None

    def refresh(self):
        print("Refreshing url: {}\n".format(self.browser.current_url))
        self.browser.get(self.browser.current_url)

    def isLoggedIn(self):
        # make sure tinder website is loaded for the first time
        if not "tinder" in self.browser.current_url:
            self.browser.get(self.HOME_URL)
            time.sleep(1.5)

        if "tinder.com/app/" in self.browser.current_url:
            return True
        else:
            print("User is not logged in yet.\n")
            return False
