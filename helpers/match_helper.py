from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException
import time

from helpers.match import Match
from helpers.socials import Socials

class MatchHelper:

    delay = 5

    HOME_URL = "https://www.tinder.com/app/recs"

    def __init__(self, browser):
        self.browser = browser
        if self.HOME_URL is not self.browser.current_url:
            self.browser.get(self.HOME_URL)
            time.sleep(2)

    def getAllMatches(self):
        return self.getNewMatches() + self.getChattedMatches()

    def getNewMatches(self):

        # Make sure we're in the 'new matches' tab
        try:
            xpath = '//*[@id="match-tab"]'
            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))

            new_matches_tab = self.browser.find_element_by_xpath(xpath)
            new_matches_tab.click()
            time.sleep(1)
        except TimeoutException:
            print("match tab could not be found, trying again")
            self.browser.get(self.HOME_URL)
            time.sleep(1)
            return self.getNewMatches()
        except Exception as e:
            print("An unhandled exception occured in getNewMatches:")
            print(e)

        matches = []

        # start scraping new matches
        try:
            xpath = '//*[@id="matchListNoMessages"]'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))

            div = self.browser.find_element_by_xpath(xpath)

            list_refs = div.find_elements_by_class_name('matchListItem')

            chatids = []

            for index in range(len(list_refs)):
                ref = list_refs[index].get_attribute('href')
                if index == 0 and ref == "https://tinder.com/app/likes-you":
                    continue
                else:
                    chatids.append(ref.split('/')[-1])

            print("\n\nScraping matches can take a while!\n")
            for index, chatid in enumerate(chatids):
                print("{}/{} of the new matches scraped".format(index, len(chatids)))
                matches.append(self.getMatch(chatid))

            return matches

        except Exception as e:
            print("getMatches FAILED for reason:\n%s" % str(e))
            return matches

    def getChattedMatches(self):
        # Make sure we're in the 'messaged matches' tab
        try:
            xpath = '//*[@id="messages-tab"]'
            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))

            messagesTab = self.browser.find_element_by_xpath(xpath)
            messagesTab.click()
            time.sleep(1)

        except TimeoutException:
            print("match tab could not be found, trying again")
            self.browser.get(self.HOME_URL)
            time.sleep(1)
            return self.getChattedMatches()
        except Exception as e:
            print("An unhandled exception occured in getNewMatches:")
            print(e)

        matches = []

        # Start scraping the chatted matches
        try:
            class_name = 'messageList'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.CLASS_NAME, class_name)))

            div = self.browser.find_element_by_class_name(class_name)

            list_refs = div.find_elements_by_class_name('messageListItem')

            chatids = []

            for index in range(len(list_refs)):
                ref = list_refs[index].get_attribute('href')
                chatids.append(ref.split('/')[-1])

            print("\n\nScraping matches can take a while!\n")
            for index, chatid in enumerate(chatids):
                print("{}/{} of the chatted matches scraped".format(index, len(chatids)))
                matches.append(self.getMatch(chatid))

            return matches

        except Exception as e:
            print("getChattedMatches FAILED for reason:\n%s" % str(e))
            return matches

    def sendMessage(self, chatid, message):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

        # locate the textbox and send message
        try:
            textbox = self.browser.find_element_by_id("chat-text-area")
            textbox.send_keys(message)
            textbox.send_keys(Keys.ENTER)
        except Exception as e:
            print("SOMETHING WENT WRONG LOCATING TEXTBOX")
            print(e)

    def sendGif(self, chatid, gifname):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

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

    def sendSong(self, chatid, songname):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

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

    def sendSocials(self, chatid, media, value):
        didMatch = False
        for social in (Socials):
            if social == media:
                didMatch = True

        if not didMatch: print("Media must be of type Socials"); return

        if not self.isChatOpened(chatid):
            self.openChat(chatid)

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
                self.sendSocials(chatid=chatid, media=media, value=value)
            except TimeoutException:
                print("There was already a value assigned to your social")

            # locate the sendbutton and send social
            try:
                self.browser.find_element_by_xpath("//button[@type='submit']").click()
                print("Succesfully send social card")
            except Exception as e:
                print("SOMETHING WENT WRONG LOCATING TEXTBOX")
                print(e)

        except Exception as e:
            print(e)

    def unMatch(self, chatid):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

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

    def openChat(self, chatid):
        href = "/app/messages/{}".format(chatid)

        # look for the match with that chatid
        # first we're gonna look for the match in the already interacted matches
        try:
            xpath = '//*[@id="messages-tab"]'
            messagesTab = self.browser.find_element_by_xpath(xpath)
            messagesTab.click()
            time.sleep(1)
        except Exception as e:
            self.browser.get(self.HOME_URL)
            print("openchat 1:" + str(e))
            return self.openChat(chatid)

        try:
            matchButton = self.browser.find_element_by_xpath('//a[@href="{}"]'.format(href))
            self.browser.execute_script("arguments[0].click();", matchButton)

        except Exception as e:
            print("openchat 2:" + str(e))
            # match reference not found, so let's see if match exists in the new not yet interacted matches
            xpath = '//*[@id="match-tab"]'
            newMatchesTab = self.browser.find_element_by_id(xpath)
            newMatchesTab.click()
            time.sleep(1)

            try:
                matchedButton = self.browser.find_element_by_xpath('//a[@href="' + href + '"]')
                matchedButton.click()
            except Exception as e:
                # some kind of error happened, probably cuz chatid/ref/match doesnt exist (anymore)
                # Another error could be that the elements could not be found, cuz we're at a wrong url (potential bug)
                print("openchat 3:" + str(e))
        time.sleep(1)

    def getMatch(self, chatid):
        if not self.isChatOpened(chatid):
            print("opening chat %s" % chatid)
            self.openChat(chatid)

        name = self.getName(chatid)
        age = self.getAge(chatid)
        distance = self.getDistance(chatid)
        bio = self.getBio(chatid)
        image_urls = self.getImageURLS(chatid)

        return Match(name=name, chatid=chatid, age=age, distance=distance, bio=bio, image_urls=image_urls)

    def getName(self, chatid):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

        try:
            element = self.browser.find_element_by_xpath('//h1[@itemprop="name"]')
            return element.text
        except Exception as e:
            print("name")
            print(e)

    def getAge(self, chatid):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

        try:
            element = self.browser.find_element_by_xpath('//span[@itemprop="age"]')
            return element.text
        except Exception as e:
            print("age")
            print(e)

    def getDistance(self, chatid):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

        try:
            element = self.browser.find_element_by_xpath("//*[contains(text(), 'kilometres away')]")
            return element.text.split(' ')[0]
        except Exception as e:
            print("distance")
            print(e)

    def getBio(self, chatid):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

        try:
            xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div'
            return self.browser.find_element_by_xpath(xpath).text
        except Exception as e:
            # no bio included?
            return None

    def getImageURLS(self, chatid):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

        image_urls = []

        try:

            classname = 'bullet'
            image_btns = self.browser.find_elements_by_class_name(classname)

            for btn in image_btns:
                btn.click()
                time.sleep(1.5)

                elements = self.browser.find_elements_by_xpath("//div[@aria-label='Profile slider']")
                for element in elements:
                    image_url = element.value_of_css_property('background-image').split('\"')[1]
                    if image_url not in image_urls:
                        image_urls.append(image_url)

            return image_urls

        except StaleElementReferenceException:
            return image_urls

        except Exception as e:
            print("unhandled exception getImageUrls in geomatch_helper")
            print(e)
            return image_urls

    def isChatOpened(self, chatid):
        # open the correct user if not happened yet
        if chatid in self.browser.current_url:
            return True
        else:
            return False