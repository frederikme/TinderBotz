from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
import time, sys

from tinderbot.helpers.match import Match
from tinderbot.helpers.socials import Socials


class MatchHelper:

    delay = 5

    HOME_URL = "https://www.tinder.com/app/recs"

    def __init__(self, browser):
        self.browser = browser
        if self.HOME_URL is not self.browser.current_url:
            self.browser.get(self.HOME_URL)
            time.sleep(2)

    def getAllMatches(self, lat_scraper, long_scraper):
        print("\n\nScraping matches can take a while!\n")
        return self.getNewMatches(lat_scraper, long_scraper) + self.getMessagedMatches(lat_scraper, long_scraper)

    def getNewMatches(self, lat_scraper, long_scraper):

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
            return self.getNewMatches(lat_scraper, long_scraper)
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

            print("\nGetting not-interacted-with, NEW MATCHES")
            for index, chatid in enumerate(chatids):
                matches.append(self.getMatch(chatid, lat_scraper=lat_scraper, long_scraper=long_scraper))

                sys.stdout.write('\r')

                amount_of_loadingbars = 30
                percentage_loaded = int((index+1/len(chatids))*100)

                # [===>----] 45% of new matches scraped
                amount_of_equals = int(percentage_loaded/100 * amount_of_loadingbars)
                amount_of_minus = amount_of_loadingbars - amount_of_equals - 1

                printout = "[{}>{}] {}%% of new matches scraped".format('='*amount_of_equals, '-'*amount_of_minus, percentage_loaded)

                sys.stdout.write(printout)
                sys.stdout.flush()
                time.sleep(0.25)

            print("\n")
        except NoSuchElementException:
            pass

        return matches

    def getMessagedMatches(self, lat_scraper, long_scraper):
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
            return self.getMessagedMatches(lat_scraper=lat_scraper, long_scraper=long_scraper)
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

            print("\nGetting interacted-with, MESSAGED MATCHES")
            for index, chatid in enumerate(chatids):
                matches.append(self.getMatch(chatid, lat_scraper=lat_scraper, long_scraper=long_scraper))

                sys.stdout.write('\r')

                amount_of_loadingbars = 30
                percentage_loaded = int((index + 1 / len(chatids)) * 100)

                # [===>----] 45% of new matches scraped
                amount_of_equals = int(percentage_loaded / 100 * amount_of_loadingbars)
                amount_of_minus = amount_of_loadingbars - amount_of_equals - 1

                printout = "[{}>{}] {}%% of messaged matches scraped".format('=' * amount_of_equals, '-' * amount_of_minus,
                                                                        percentage_loaded)
                sys.stdout.write(printout)
                sys.stdout.flush()
                time.sleep(0.25)
            print("\n")
        except NoSuchElementException:
            pass

        except TimeoutException:
            pass

        return matches

    def sendMessage(self, chatid, message):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

        # locate the textbox and send message
        try:
            xpath = '//*[@id="chat-text-area"]'

            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH,xpath)))

            textbox = self.browser.find_element_by_xpath(xpath)
            textbox.send_keys(message)
            textbox.send_keys(Keys.ENTER)

            print("Message sent succesfully.\nmessage: {}\n".format(message))

            # sleep so message can be sent
            time.sleep(1.5)
        except Exception as e:
            print("SOMETHING WENT WRONG LOCATING TEXTBOX")
            print(e)

    def sendGif(self, chatid, gifname):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

        try:
            xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[1]/button'

            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            gif_btn = self.browser.find_element_by_xpath(xpath)

            gif_btn.click()
            time.sleep(1.5)

            search_box = self.browser.find_element_by_xpath('//*[@id="chat-text-area"]')
            search_box.send_keys(gifname)
            # give chance to load gif
            time.sleep(1.5)

            gif = self.browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div/div[1]/div[1]/div')
            gif.click()
            # sleep so gif can be sent
            time.sleep(1.5)

        except Exception as e:
            print(e)

    def sendSong(self, chatid, songname):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

        try:
            xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[2]/button'

            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            song_btn = self.browser.find_element_by_xpath(xpath)

            song_btn.click()
            time.sleep(1.5)

            search_box = self.browser.find_element_by_xpath('//*[@id="chat-text-area"]')
            search_box.send_keys(songname)
            # give chance to load gif
            time.sleep(1.5)

            song = self.browser.find_element_by_xpath(
                '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[2]/div/div[1]/div[1]/div/div[1]/div/button')
            song.click()
            time.sleep(0.5)

            confirm_btn = self.browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[2]/div/div[1]/div[1]/div/div[2]/button')
            confirm_btn.click()
            # sleep so song can be sent
            time.sleep(1.5)

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
            xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/div/div[3]/button'

            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            socials_btn = self.browser.find_element_by_xpath(xpath)

            socials_btn.click()
            time.sleep(1.5)

            social_btn = self.browser.find_element_by_xpath('//div[@data-cy-type="{}"]'.format(media.value))
            social_btn.click()

            # check if name needs to be given or not
            try:
                contactcard_xpath = "//input[@aria-labelledby='contact-card-input-label']"

                WebDriverWait(self.browser, 2).until(EC.presence_of_element_located((By.XPATH, contactcard_xpath)))

                input = self.browser.find_element_by_xpath(contactcard_xpath)
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
                # sleep so message can be sent
                time.sleep(1.5)
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
        if self.isChatOpened(chatid): return;

        href = "/app/messages/{}".format(chatid)

        # look for the match with that chatid
        # first we're gonna look for the match in the already interacted matches
        try:
            xpath = '//*[@id="messages-tab"]'
            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))

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
            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))

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

    def getMatch(self, chatid, lat_scraper, long_scraper):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

        name = self.getName(chatid)
        age = self.getAge(chatid)
        distance = self.getDistance(chatid)
        bio = self.getBio(chatid)
        image_urls = self.getImageURLS(chatid)

        return Match(name=name, chatid=chatid, age=age, distance=distance, bio=bio, image_urls=image_urls,
                     lat_scraper=lat_scraper, long_scraper=long_scraper)

    def getName(self, chatid):
        if not self.isChatOpened(chatid):
            self.openChat(chatid)

        try:
            xpath = '//h1[@itemprop="name"]'
            element = self.browser.find_element_by_xpath(xpath)
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
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
            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.CLASS_NAME, classname)))

            image_btns = self.browser.find_elements_by_class_name(classname)

            for btn in image_btns:
                btn.click()
                time.sleep(1)

                elements = self.browser.find_elements_by_xpath("//div[@aria-label='Profile slider']")
                for element in elements:
                    image_url = element.value_of_css_property('background-image').split('\"')[1]
                    if image_url not in image_urls:
                        image_urls.append(image_url)

        except StaleElementReferenceException:
            pass

        except TimeoutException:
            pass

        except Exception as e:
            print("unhandled exception getImageUrls in match_helper")
            print(e)

        return image_urls

    def isChatOpened(self, chatid):
        # open the correct user if not happened yet
        if chatid in self.browser.current_url:
            return True
        else:
            return False