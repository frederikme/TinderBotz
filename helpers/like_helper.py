from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class LikeHelper:

    delay = 3

    HOME_URL = "https://www.tinder.com/app/recs"

    def __init__(self, browser):
        self.browser = browser
        if self.HOME_URL not in self.browser.current_url:
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

            except TimeoutException:
                # like button not found -> reload page to find button again
                print("YOU GOT A NEW MATCH")
                # reload page so pop up of match disappears
                self.browser.get(self.HOME_URL)

            except Exception as e:
                print("Another, not handled, exception occurred at like")
                print(e)

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

        except TimeoutException:
            # dislike button not found -> reload page to find button again
            print("dislike button not found -> reloading home page to find button again")
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

        except TimeoutException:
            # superlike button not found -> reload page to find button again
            print("superlike button not found -> reloading page and trying again")
            self.browser.get(self.HOME_URL)
            self.superlike(amount=amount)

        except Exception as e:
            print("Another, not handled, exception occurred at superlike")
            print(e)
