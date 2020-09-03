from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
# for our print statements and layout in terminal/command prompt
import pyfiglet
import os
import time
from helpers.login_helper import LoginHelper
from helpers.match import Match

class TinderBot:

    delay = 5

    def __init__(self):
        self.logToScreen("Tinderbot", isBanner=True)
        self.logToScreen("-> Made by Frederikme")
        self.logToScreen("-----------------------------------\n\n")

        self.logToScreen("Getting ChromeDriver ...")
        self.browser = webdriver.Chrome(ChromeDriverManager().install())


    def loadPage(self, url):
        self.logToScreen("Loading page %s" % str(url))
        self.browser.get(url)
        # optionally add storage and readability of cookies with pickle

    def loginUsingGoogle(self, email, password):
        helper = LoginHelper(browser=self.browser)
        helper.loginByGoogle(email, password)

    def loginUsingFacebook(self, email, password):
        helper = LoginHelper(browser=self.browser)
        helper.loginByFacebook(email, password)

    def like(self, amount=1):
        like_button = self.browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')

        for _ in range(amount):
            like_button.click()
            time.sleep(1)
            # if you don't want the script to crash make sure you -> set gotMatched on return True
            # for a smooth run without having to refresh the browser after every like -> set gotMatched on return False
            if self.gotMatched():
                self.backToTinder()  # or TODO: self.sendMessageToFreshMatched()

    def gotMatched(self):
        # TODO check if there was a match ( hard to do, since I don't get any matches :')
        return False

    def backToTinder(self):
        self.browser.get('http://www.tinder.com')
        time.sleep(2)
        return

    def dislike(self, amount=1):
        dislike_button = self.browser.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')

        for _ in range(amount):
            dislike_button.click()
            time.sleep(1)

    def superlike(self, amount=1):
        superlike_button = self.browser.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[3]/button')

        for _ in range(amount):
            superlike_button.click()
            time.sleep(1)


    def getMatches(self):
        try:
            div = self.browser.find_element_by_id('matchListNoMessages')

            list_refs = div.find_elements_by_class_name('matchListItem')
            list_names = div.find_elements_by_class_name('Ell')

            if len(list_refs) < len(list_names): length = len(list_refs)
            else: length = len(list_names)

            needed_minus_one_in_name_index = False

            matches = []

            for index in range(length):
                ref = list_refs[index].get_attribute('href')
                if index == 0 and ref == "https://tinder.com/app/likes-you":
                    needed_minus_one_in_name_index = True
                    continue
                else:
                    if needed_minus_one_in_name_index:
                        name = list_names[index-1].text
                    else:
                        name = list_names[index].text


                matches.append(Match(name=name, mref=ref))

            return matches

        except Exception as e:
            print("getMatches FAILED for reason:\n%s" % str(e))
            return []

    def logToScreen(self, text, isBanner=False):
        if isBanner:
            # clear the terminal
            os.system("clear")
            banner = pyfiglet.figlet_format(text)
        else:
            # provide one line space in between
            print("\n")
            banner = text

        print(banner)
        # give time to let the shown message in console sink in
        time.sleep(1)