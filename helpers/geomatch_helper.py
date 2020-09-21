from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import time

from helpers.geomatch import Geomatch

class GeomatchHelper:

    delay = 3

    HOME_URL = "https://www.tinder.com/app/recs"

    def __init__(self, browser):
        self.browser = browser
        if self.HOME_URL is not self.browser.current_url:
            self.browser.get(self.HOME_URL)

    def like(self, amount):
        for _ in range(amount):
            try:
                xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button'

                # wait for element to appear
                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

                # locate like button
                like_button = self.browser.find_element_by_xpath(xpath)

                like_button.click()
                time.sleep(1)

            except ElementClickInterceptedException:
                # popup is blocking the like button -> reload page to find button again
                print("YOU GOT A NEW MATCH")
                # reload page so pop up of match disappears
                self.browser.get(self.HOME_URL)
                continue
            except TimeoutException:
                # like button not found in time -> reload page to find button again
                print("dislike button not found -> reloading home page to find button again")
                self.browser.get(self.HOME_URL)
                self.dislike(amount=amount)
                break
            except Exception as e:
                print("Another, not handled, exception occurred at like")
                print(e)
                break

    def dislike(self, amount):
        try:
            xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

            dislike_button = self.browser.find_element_by_xpath(xpath)

            for _ in range(amount):
                dislike_button.click()
                time.sleep(0.5)

        except ElementClickInterceptedException:
            # popup is blocking the dislike button -> reload page to find button again
            print("Needs to reload page")
            # reload page so pop up of match disappears
            self.browser.get(self.HOME_URL)

        except TimeoutException:
            # dislike button not found in time -> reload page to find button again
            print("dislike button not found in time -> reloading home page to find button again")
            self.browser.get(self.HOME_URL)
            self.dislike(amount=amount)

        except Exception as e:
            print("Another, not handled, exception occurred at dislike")
            print(e)

    def superlike(self, amount):
        try:
            xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[3]/div/div/div/button'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            superlike_button = self.browser.find_element_by_xpath(xpath)

            for _ in range(amount):
                superlike_button.click()
                time.sleep(0.5)

        except ElementClickInterceptedException:
            # popup is blocking the superlike button -> reload page to find button again
            print("Needs to reload page")
            # reload page so pop up of match disappears
            self.browser.get(self.HOME_URL)

        except TimeoutException:
            # superlike button not found in time -> reload page to find button again
            print("superlike button not found in time -> reloading page and trying again")
            self.browser.get(self.HOME_URL)
            self.superlike(amount=amount)

        except Exception as e:
            print("Another, not handled, exception occurred at superlike")
            print(e)

    def openProfile(self, second_try=False):
        if self.isProfileOpened(): return;
        try:
            xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/button'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            full_profile_button = self.browser.find_element_by_xpath(xpath)

            full_profile_button.click()

        except TimeoutException:
            if not second_try:
                print("Trying again to locate the profile info button in a second")
                time.sleep(2)
                self.openProfile(second_try=True)
            else:
                print("timeout exception")

        except Exception as e:
            print("exception")
            print(e)

    def getName(self):
        if not self.isProfileOpened():
            self.openProfile()

        try:
            element = self.browser.find_element_by_xpath('//h1[@itemprop="name"]')
            return element.text
        except Exception as e:
            print("name")
            print(e)

    def getAge(self):
        if not self.isProfileOpened():
            self.openProfile()

        try:
            element = self.browser.find_element_by_xpath('//span[@itemprop="age"]')
            return element.text
        except Exception as e:
            print("age")
            print(e)

    def getDistance(self):
        if not self.isProfileOpened():
            self.openProfile()

        try:
            element = self.browser.find_element_by_xpath("//*[contains(text(), 'kilometres away')]")
            return element.text.split(' ')[0]
        except Exception as e:
            print("distance")
            print(e)

    def getBio(self):
        if not self.isProfileOpened():
            self.openProfile()

        try:
            xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div'
            return self.browser.find_element_by_xpath(xpath).text
        except Exception as e:
            # no bio included?
            return None

    def getImageURLS(self):
        if not self.isProfileOpened():
            self.openProfile()

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

    def isProfileOpened(self):
        if '/profile' in self.browser.current_url:
            return True
        else:
            return False