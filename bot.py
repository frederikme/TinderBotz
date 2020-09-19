from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import urllib.request
from PIL import Image

import pyfiglet
import os
import json
import time
from helpers.login_helper import LoginHelper
from helpers.like_helper import LikeHelper
from helpers.match import Match
from helpers.socials import Socials

class TinderBot:

    delay = 5

    HOME_URL = "https://www.tinder.com/app/recs"

    def __init__(self):
        self.logToScreen("Tinderbot", isBanner=True)
        self.logToScreen("-> Made by Frederikme")
        self.logToScreen("-----------------------------------\n\n")

        self.logToScreen("Getting ChromeDriver ...")
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def loadPage(self, url):
        self.logToScreen("Loading page %s" % str(url))
        self.browser.get(url)
        time.sleep(1.5)

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
            helper = LikeHelper(browser=self.browser)
            helper.like(amount)

    def dislike(self, amount=1):
        if self.isLoggedIn():
            helper = LikeHelper(browser=self.browser)
            helper.dislike(amount)

    def superlike(self, amount=1):
        if self.isLoggedIn():
            helper = LikeHelper(browser=self.browser)
            helper.superlike(amount)

    def getAllMatches(self, store_local=True):
        new_matches = self.getNewMatches()
        changed_matches = self.getChattedMatches()

        all_matches = new_matches + changed_matches

        if store_local:
            data = {'matches': []}

            for match in all_matches:
                match_data = {
                    "name": match.getName(),
                    "id": match.getID()
                }
                data['matches'].append(match_data)

            json_data = json.dumps(data)

            with open('data/matches.json', 'w') as file:
                json.dump(json_data, file)

        return all_matches

    def getNewMatches(self):
        try:
            newMatchesTab = self.browser.find_element_by_id("match-tab")
            newMatchesTab.click()
            time.sleep(1)
        except:
            print("match tab could not be found, trying again")
            time.sleep(1)
            self.loadPage(self.HOME_URL)
            return self.getNewMatches()

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

    def getChattedMatches(self):
        try:
            messagesTab = self.browser.find_element_by_id("messages-tab")
            messagesTab.click()
            time.sleep(1)
        except:
            print("messages tab could not be found, trying again")
            time.sleep(1)
            self.loadPage(self.HOME_URL)
            return self.getChattedMatches()

        try:
            div = self.browser.find_element_by_class_name('messageList')

            list_refs = div.find_elements_by_class_name('messageListItem')
            list_names = div.find_elements_by_class_name('messageListItem__name')

            # length of 2 lists should always be equal btw
            length = len(list_refs)


            matches = []

            for index in range(length):
                ref = list_refs[index].get_attribute('href')
                name = list_names[index].text
                matches.append(Match(name=name, mref=ref))

            return matches

        except Exception as e:
            print("getMatches FAILED for reason:\n%s" % str(e))
            return []

    def openChat(self, id):
        href = "/app/messages/%s" % id

        # look for the match with that id
        # first we're gonna look for the match in the already interacted matches
        try:
            messagesTab = self.browser.find_element_by_id("messages-tab")
            messagesTab.click()
            time.sleep(1)
        except:
            self.loadPage(self.HOME_URL)
            return self.openChat(id)

        try:
            matchButton = self.browser.find_element_by_xpath('//a[@href="' + href + '"]')
            matchButton.click()
        except:

            # match reference not found, so let's see if match exists in the new not yet interacted matches
            newMatchesTab = self.browser.find_element_by_id("match-tab")
            newMatchesTab.click()
            time.sleep(1)

            try:
                matchedButton = self.browser.find_element_by_xpath('//a[@href="' + href + '"]')
                matchedButton.click()
            except Exception as e:
                # some kind of error happened, probably cuz id/ref/match doesnt exist (anymore)
                # Another error could be that the elements could not be found, cuz we're at a wrong url (potential bug)
                print(e)
        time.sleep(1)

    def sendMessage(self, id, message):
        # open the correct chat if not happened yet
        if id not in self.browser.current_url:
            self.openChat(id)
            time.sleep(1)

        # locate the textbox and send message
        try:
            textbox = self.browser.find_element_by_id("chat-text-area")
            textbox.send_keys(message)
            textbox.send_keys(Keys.ENTER)
        except Exception as e:
            print("SOMETHING WENT WRONG LOCATING TEXTBOX")
            print(e)

    def sendGif(self, id, gifname):
        # open the correct chat if not happened yet
        if id not in self.browser.current_url:
            self.openChat(id)
            time.sleep(1)

        try:
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[1]/button')))
            gif_btn = self.browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[1]/button')

            gif_btn.click()
            time.sleep(1.5)

            search_box = self.browser.find_element_by_id('chat-text-area')
            search_box.send_keys(gifname)
            # give chance to load gif
            time.sleep(1.5)

            gif = self.browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div/div[1]/div[1]/div')
            gif.click()

        except Exception as e:
            print(e)

    def sendSong(self, id, songname):
        # open the correct chat if not happened yet
        if id not in self.browser.current_url:
            self.openChat(id)
            time.sleep(1)

        try:
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[2]/button')))
            song_btn = self.browser.find_element_by_xpath(
                '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[2]/button')

            song_btn.click()
            time.sleep(1.5)

            search_box = self.browser.find_element_by_id('chat-text-area')
            search_box.send_keys(songname)
            # give chance to load gif
            time.sleep(1.5)

            song = self.browser.find_element_by_xpath(
                '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[2]/div/div[1]/div[1]/div/div[1]/div/button')
            song.click()
            time.sleep(0.5)

            confirm_btn = self.browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[2]/div/div[1]/div[1]/div/div[2]/button')
            confirm_btn.click()

        except Exception as e:
            print(e)

    def sendSocials(self, id, media, value="Teeti.fm"):
        didMatch = False
        for social in (Socials):
            if social == media:
                didMatch = True

        if not didMatch: print("Media must be of type Socials"); return

        # open the correct chat if not happened yet
        if id not in self.browser.current_url:
            self.openChat(id)
            time.sleep(1)

        try:
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[3]/button')))
            socials_btn = self.browser.find_element_by_xpath(
                '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[3]/button')

            socials_btn.click()
            time.sleep(1.5)

            social_btn = self.browser.find_element_by_xpath('//div[@data-cy-type="{}"]'.format(media.value))
            social_btn.click()

            # check if name needs to be given or not
            try:
                WebDriverWait(self.browser, 2).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='contact-card-input-label']")))

                input = self.browser.find_element_by_xpath("//input[@aria-labelledby='contact-card-input-label']")
                input.send_keys(value)

                confirm_btn = self.browser.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[3]/button[1]')
                confirm_btn.click()

                # resend with saved value this time
                self.sendSocials(id=id, media=media, value=value)
            except TimeoutException:
                print("There was already a value assigned to your social")

            # locate the sendbutton and send social
            try:
                #self.browser.find_element_by_xpath("//button[@type='submit']").click()
                print("Succesfully send social card")
            except Exception as e:
                print("SOMETHING WENT WRONG LOCATING TEXTBOX")
                print(e)

        except Exception as e:
            print(e)

    def unMatch(self, id):
        # open the correct user if not happened yet
        if id not in self.browser.current_url:
            self.openChat(id)
            time.sleep(1)

        try:
            unmatch_button = self.browser.find_element_by_xpath('//button[text()="Unmatch"]')
            unmatch_button.click()
            time.sleep(1)

            # We will unmatch the person with "no reason" as declaration
            reason_button = self.browser.find_element_by_xpath('//div[text()="No reason"]')
            reason_button.click()
            time.sleep(1)

            # scroll down so confirm
            html = self.browser.find_element_by_tag_name('html')
            html.send_keys(Keys.END)
            time.sleep(1)

            confirm_button = self.browser.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button')
            confirm_button.click()
            time.sleep(1)

        except Exception as e:
            print("SOMETHING WENT WRONG FINDING THE UNMATCH BUTTONS")
            print(e)

    def getImage(self, id, store_local=True):
        # open the correct user if not happened yet
        if id not in self.browser.current_url:
            self.openChat(id)
        try:

            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/span/div/div[1]/span[1]/div/div')))

            element = self.browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[2]/div/div[1]/div/div/div[1]/span/div/div[1]/span[1]/div/div')
            image_url = element.value_of_css_property('background-image').split('\"')[1]

        except Exception as e:
            print(e)
            return None

        if store_local:
            random_image_name = id

            if not os.path.exists("data/images"):
                os.makedirs("data/images")

            urllib.request.urlretrieve(image_url, "{}.webp".format(random_image_name))

            im = Image.open("{}.webp".format(random_image_name)).convert("RGB")
            im.save("{}/data/images/{}.jpg".format(os.getcwd(), random_image_name), "jpeg")

            os.remove("{}.webp".format(random_image_name))

        return image_url

    def isLoggedIn(self):
        # make sure tinder website is loaded for the first time
        if not "tinder" in self.browser.current_url:
            self.loadPage(self.HOME_URL)

        if "tinder.com/app/" in self.browser.current_url:
            return True
        else:
            print("User is not logged in yet.")
            return False

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