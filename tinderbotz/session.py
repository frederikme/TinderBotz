# Selenium: automation of browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException

# some
import pyfiglet # Let's us create
import os
from sys import platform
import time
import random
import atexit

# Tinderbotz: helper classes
from tinderbotz.helpers.geomatch import Geomatch
from tinderbotz.helpers.match import Match
from tinderbotz.helpers.location_helper import LocationHelper
from tinderbotz.helpers.profile_helper import ProfileHelper
from tinderbotz.helpers.geomatch_helper import GeomatchHelper
from tinderbotz.helpers.match_helper import MatchHelper
from tinderbotz.helpers.login_helper import LoginHelper
from tinderbotz.helpers.storage_helper import StorageHelper
from tinderbotz.helpers.loadingbar import LoadingBar
from tinderbotz.helpers.email_helper import EmailHelper


class Session:

    HOME_URL = "https://www.tinder.com/app/recs"

    def __init__(self):
        # clear the console based on the operating system you're using
        if platform == "linux" or platform == "linux2" or "darwin":
            os.system("clear")
        elif platform == "win32":
            os.system("cls")

        # Cool banner
        title = ''' 
         _____ _           _           _           _       
        |_   _(_)_ __   __| | ___ _ __| |__   ___ | |_ ____
          | | | | '_ \ / _` |/ _ \ '__| '_ \ / _ \| __|_  /
          | | | | | | | (_| |  __/ |  | |_) | (_) | |_ / / 
          |_| |_|_| |_|\__,_|\___|_|  |_.__/ \___/ \__/___|
        ----------------------------------------------------'''
        print(title)
        print("Made by Frederikme")
        y = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("Started session: {}\n\n".format(y))

        self.email = None
        self.may_send_email = False
        self.session_data = {
            "duration": 0,
            "like": 0,
            "dislike": 0,
            "superlike": 0
        }

        start_session = time.time()

        # this function will run when the session ends
        @atexit.register
        def cleanup():
            # End session duration
            seconds = int(time.time() - start_session)
            self.session_data["duration"] = seconds

            # add key's to list
            lines = []
            for key in self.session_data:
                message = "{}: {}".format(key, self.session_data[key])
                lines.append(message)

            # print out stats of the session
            try:
                box = self.msg_box(lines=lines, title="Tinderbotz")
                print(box)
            finally:
                y = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print("Ended session: {}".format(y))

        # Go further with the initialisation
        # add location guard extension as option parameter
        print("Adding Location Guard extension ...")
        options = webdriver.ChromeOptions()
        options.add_extension('./tinderbotz/LocationGuardExtension.crx')
        options.add_experimental_option('w3c', False)

        # getting chromedriver from cache or download from internet
        print("Getting ChromeDriver ...")
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.browser.set_window_size(1250, 750)

        # wait some time, before location guard extension pops up in second tab then close it
        time.sleep(2)
        self.closeAbundantTabs()

    def closeAbundantTabs(self):
        # close all other tabs
        while len(self.browser.window_handles) > 1:
            current_window = self.browser.current_window_handle
            other_window = self.browser.window_handles[1]
            self.browser.switch_to.window(other_window)
            self.browser.close()
            self.browser.switch_to.window(current_window)

    # Setting the users location using the downloaded chrome extension Location Guard
    # Don't need to be logged in for this.
    def setCustomLocation(self, location_name):
        helper = LocationHelper(browser=self.browser)
        helper.setCustomLocation(location_name)

    def setRealtimeLocation(self):
        helper = LocationHelper(browser=self.browser)
        helper.setRealtimeLocation()

    # This will send notification when you get a match to your email used to logged in.
    def setEmailNotifications(self, boolean):
        self.may_send_email = boolean

    # NOTE: Need to be logged in for this
    def setDistanceRange(self, km):
        helper = ProfileHelper(browser=self.browser)
        helper.setDistanceRange(km)

    def setAgeRange(self, min, max):
        helper = ProfileHelper(browser=self.browser)
        helper.setAgeRange(min, max)

    def setSexuality(self, type):
        helper = ProfileHelper(browser=self.browser)
        helper.setSexualitiy(type)

    def setGlobal(self, boolean):
        helper = ProfileHelper(browser=self.browser)
        helper.setGlobal(boolean)

    # Actions of the session
    def loginUsingGoogle(self, email, password):
        self.email = email
        if not self.isLoggedIn():
            helper = LoginHelper(browser=self.browser)
            helper.loginByGoogle(email, password)

    def loginUsingFacebook(self, email, password):
        self.email = email
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

    def like(self, amount=1, ratio='100%', sleep=0):

        ratio = float(ratio.split('%')[0]) / 100

        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)
            loadingbar = LoadingBar(amount, "likes")
            amount_liked = 0
            # handle one time up front, from then on check after every action instead of before
            self.handlePotentialPopups()
            while amount_liked < amount:
                if random.random() <= ratio:
                    helper.like()
                    amount_liked += 1

                    # update for stats after session ended
                    self.session_data['like'] += 1

                    # update loadingbar display
                    loadingbar.updateLoadingBar(amount_liked)

                else:
                    helper.dislike()

                    # update for stats after session ended
                    self.session_data['dislike'] += 1

                self.handlePotentialPopups()
                time.sleep(sleep)

    def dislike(self, amount=1):
        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)
            loadingbar = LoadingBar(amount, "dislikes")
            for index in range(amount):
                self.handlePotentialPopups()
                helper.dislike()

                # update for stats after session ended
                self.session_data['dislike'] += 1

                # update loadingbar display
                loadingbar.updateLoadingBar(index)

    def superlike(self, amount=1):
        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)
            loadingbar = LoadingBar(amount, "superlikes")
            for index in range(amount):
                self.handlePotentialPopups()
                helper.superlike()
                # update for stats after session ended
                self.session_data['dislike'] += 1

                # update loadingbar display
                loadingbar.updateLoadingBar(index)

    def getGeomatch(self):
        if self.isLoggedIn():
            helper = GeomatchHelper(browser=self.browser)
            self.handlePotentialPopups()

            name = None
            attempts = 0
            max_attempts = 20
            while not name and attempts < max_attempts:
                attempts += 1
                name = helper.getName()
                time.sleep(2)

            age = helper.getAge()
            distance = helper.getDistance()
            bio = helper.getBio()
            image_urls = helper.getImageURLS()

            return Geomatch(name=name, age=age, distance=distance, bio=bio, image_urls=image_urls)

    def getAllMatches(self):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            return helper.getAllMatches()

    def getNewMatches(self):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            return helper.getNewMatches()

    def getMessagedMatches(self):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            return helper.getMessagedMatches()

    def sendMessage(self, chatid, message):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            helper.sendMessage(chatid, message)

    def sendGif(self, chatid, gifname):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            helper.sendGif(chatid, gifname)

    def sendSong(self, chatid, songname):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            helper.sendSong(chatid, songname)

    def sendSocials(self, chatid, media, value):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            helper.sendSocials(chatid, media, value)

    def unMatch(self, chatid):
        if self.isLoggedIn():
            helper = MatchHelper(browser=self.browser)
            self.handlePotentialPopups()
            helper.unMatch(chatid)

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

        # Try to dismiss a potential 'upgrade like' popup
        try:
            # locate "no thanks"-button
            xpath = '//*[@id="modal-manager"]/div/div/button[2]'
            self.browser.find_element_by_xpath(xpath).click()
            return "POPUP: Denied upgrade to superlike"
        except NoSuchElementException:
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
        matched = False
        try:
            xpath = '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[4]/button'

            match_popup = self.browser.find_element_by_xpath(xpath)
            match_popup.click()
            matched = True

        except NoSuchElementException:
            pass

        if matched and self.may_send_email:

            try:
                EmailHelper.sendMailMatchFound(self.email)
            except:
                print("Some error occurred when trying to send mail.")
                print("Consider opening an Issue on Github.")
                pass
            return "POPUP: Dismissed NEW MATCH"

        # try to say 'no thanks' to buy more (super)likes
        try:
            xpath = '//*[@id="modal-manager"]/div/div/div[3]/button[2]'
            denyBtn = self.browser.find_element_by_xpath(xpath)
            denyBtn.click()
            return "POPUP: Denied buying more superlikes"

        except ElementNotVisibleException:
            # element is not clickable, probably cuz it's out of view but still there
            self.browser.refresh()
        except NoSuchElementException:
            pass

        # Deny confirmation of email
        try:
            xpath = '//*[@id="modal-manager"]/div/div/div[1]/div[2]/button[2]'
            remindmelater = self.browser.find_element_by_xpath(xpath)
            remindmelater.click()

            time.sleep(3)
            # handle other potential popups
            self.handlePotentialPopups()

            return "POPUP: Deny confirmation of email"
        except:
            pass

        return None

    def isLoggedIn(self):
        # make sure tinder website is loaded for the first time
        if not "tinder" in self.browser.current_url:
            # enforce english language
            self.browser.get("https://tinder.com/?lang=en")
            time.sleep(1.5)

        if "tinder.com/app/" in self.browser.current_url:
            return True
        else:
            print("User is not logged in yet.\n")
            return False

    def msg_box(self, lines, indent=1, width=None, title=None):
        """Print message-box with optional title."""
        space = " " * indent
        if not width:
            width = max(map(len, lines))
        box = f'/{"=" * (width + indent * 2)}\\\n'  # upper_border
        if title:
            box += f'|{space}{title:<{width}}{space}|\n'  # title
            box += f'|{space}{"-" * len(title):<{width}}{space}|\n'  # underscore
        box += ''.join([f'|{space}{line:<{width}}{space}|\n' for line in lines])
        box += f'\\{"=" * (width + indent * 2)}/'  # lower_border
        return box