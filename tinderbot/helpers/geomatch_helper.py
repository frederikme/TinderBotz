from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import time


class GeomatchHelper:

    delay = 3

    HOME_URL = "https://www.tinder.com/app/recs"

    def __init__(self, browser):
        self.browser = browser
        if "/app/recs" not in self.browser.current_url:
            self.getHomePage()

    def like(self):
        try:
            if 'profile' in self.browser.current_url:
                xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[4]/button'
            else:
                xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            # locate like button
            like_button = self.browser.find_element_by_xpath(xpath)

            like_button.click()
            time.sleep(1)

        except ElementClickInterceptedException:
            self.getHomePage()

        except TimeoutException:
            # like button not found in time -> reload page to find button again
            print("like button not found -> reloading home page to find button again")
            self.getHomePage()

        except Exception as e:
            print("Another, not handled, exception occurred at like")
            print(e)

    def dislike(self):
        try:
            # TODO handle by aria-label, cleaner and no need to diverse between profile selected or not
            if 'profile' in self.browser.current_url:
                xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[2]/button'
            else:
                xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

            dislike_button = self.browser.find_element_by_xpath(xpath)

            dislike_button.click()
            time.sleep(1)

        except ElementClickInterceptedException:
            # popup is blocking the dislike button
            self.getHomePage()

        except TimeoutException:
            # dislike button not found in time -> reload page to find button again
            print("dislike button not found in time -> reloading home page to find button again")
            self.getHomePage()

        except Exception as e:
            print("Another, not handled, exception occurred at dislike")
            print(e)

    def superlike(self):
        try:
            xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[3]/div/div/div/button'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            superlike_button = self.browser.find_element_by_xpath(xpath)

            superlike_button.click()

        except ElementClickInterceptedException:
            self.getHomePage()

        except TimeoutException:
            # superlike button not found in time -> reload page to find button again
            print("superlike button not found in time -> reloading page")
            self.getHomePage()

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
            time.sleep(1)

        except TimeoutException:
            if not second_try:
                print("Trying again to locate the profile info button in a few seconds")
                time.sleep(2)
                self.openProfile(second_try=True)
            else:
                print("timeout exception")

        except Exception as e:
            print(e)

    def getName(self):
        if not self.isProfileOpened():
            self.openProfile()
            return self.getName()

        try:
            xpath = '//h1[@itemprop="name"]'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            element = self.browser.find_element_by_xpath(xpath)
            return element.text
        except Exception as e:
            print("name")
            print(e)

    def getAge(self):
        if not self.isProfileOpened():
            self.openProfile()

        try:
            xpath = '//span[@itemprop="age"]'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            element = self.browser.find_element_by_xpath(xpath)
            try:
                return int(element.text)
            except ValueError:
                return None

        except Exception as e:
            print("age")
            print(e)

    def getDistance(self):
        if not self.isProfileOpened():
            self.openProfile()

        try:

            xpath = "//*[contains(text(), 'kilometres away')]"

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            element = self.browser.find_element_by_xpath(xpath)

            distance = element.text.split(' ')[0]

            try:
                distance = int(distance)
            except TypeError:
                # Means the text has a value of 'Less than 1 km away'
                distance = 1

            return distance

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
            print(e)
            return None

    def getImageURLS(self):
        if not self.isProfileOpened():
            self.openProfile()

        image_urls = []

        try:
            # There are no bullets when there is only 1 image
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
            # there is only 1 image, so no bullets to iterate through
            try:
                element = self.browser.find_element_by_xpath("//div[@aria-label='Profile slider']")
                image_url = element.value_of_css_property('background-image').split('\"')[1]
                if image_url not in image_urls:
                    image_urls.append(image_url)

            except Exception as e:
                print("unhandled Exception when trying to store their only image")
                print(e)

        except Exception as e:
            print("unhandled exception getImageUrls in geomatch_helper")
            print(e)

        return image_urls

    def getHomePage(self):
        self.browser.get(self.HOME_URL)
        time.sleep(3)

    def isProfileOpened(self):
        if '/profile' in self.browser.current_url:
            return True
        else:
            return False