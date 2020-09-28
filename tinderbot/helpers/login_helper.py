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


class LoginHelper:

    delay = 5

    def __init__(self, browser):
        self.browser = browser

    def clickLoginButton(self):
        # check if there is a login button, if there is, that means user is not logged in yet
        try:
            xpath = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/header/div[1]/div[2]/div/button'

            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            btn = self.browser.find_element_by_xpath(xpath)

            btn.click()

            time.sleep(2)

        except Exception as e:
            print(e)

    def loginByGoogle(self, email, password):
        self.clickLoginButton()

        # wait for google button to appear
        try:
            xpath = '//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[1]/div/button'

            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            btn = self.browser.find_element_by_xpath(xpath)

            btn.send_keys(Keys.ENTER)
            print("Sleeping 3 seconds for pop up to come through")
            time.sleep(3)
        except TimeoutException:
            print("Loading took too much time! Let's try again.")
        except Exception as e:
            print("def login(self): 2: %s" % str(e))

        if not self.changeFocusToPopUp():
            print("FAILED TO CHANGE FOCUS TO POPUP")
        try:
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))

            emailfield = self.browser.find_element_by_xpath("//input[@type='email']")
            emailfield.send_keys(email)
            emailfield.send_keys(Keys.ENTER)
            print("Sleeping 3 seconds for passwordfield to come through")
            time.sleep(3)
        except TimeoutException:
            print("EMAIL: Loading took too much time! Let's try again.")

        except Exception as e:
            print("def login(self): 3: %s" % str(e))

        try:
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))

            pwdfield = self.browser.find_element_by_xpath("//input[@type='password']")
            pwdfield.send_keys(password)
            pwdfield.send_keys(Keys.ENTER)

            self.changeFocusToMainWindow()

            print("Sleeping 3 seconds before returning to main view")
            time.sleep(3)
        except TimeoutException:
            print("PASSWORD: Loading took too much time! Let's try again.")
        except Exception as e:
            print("def login(self): 4: %s" % str(e))

        self.handlePopups()

    def loginByFacebook(self, email, password):
        self.clickLoginButton()

        # wait for facebook button to appear
        try:
            xpath = '//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button'

            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            btn = self.browser.find_element_by_xpath(xpath)

            btn.send_keys(Keys.ENTER)
            print("Sleeping 3 seconds for pop up to come through")
            time.sleep(3)
        except TimeoutException:
            print("Loading took too much time! Let's try again.")
        except Exception as e:
            print("def login(self): 2: %s" % str(e))

        if not self.changeFocusToPopUp():
            print("FAILED TO CHANGE FOCUS TO POPUP")
        try:

            xpath_email = '//*[@id="email"]'
            xpath_password = '//*[@id="pass"]'
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath_email)))

            emailfield = self.browser.find_element_by_xpath(xpath_email)
            emailfield.send_keys(email)

            pwdfield = self.browser.find_element_by_xpath(xpath_password)
            pwdfield.send_keys(password)
            pwdfield.send_keys(Keys.ENTER)

            self.changeFocusToMainWindow()

            print("Sleeping 3 seconds before returning to main view")
            time.sleep(3)
        except TimeoutException:
            print("PASSWORD: Loading took too much time! Let's try again.")
        except Exception as e:
            print("def login(self): 4: %s" % str(e))

        self.handlePopups()

    def handlePopups(self):
        time.sleep(2)
        self.acceptCookies()
        self.acceptLocationNotification()
        self.denyOverlayedNotifications()
        self.denySeeWhoLikedYou()

    def acceptLocationNotification(self):
        try:
            xpath = '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]'
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))

            locationBtn = self.browser.find_element_by_xpath(xpath)
            locationBtn.click()
            print("ACCEPTED LOCATION")
            print("Sleeping 2 seconds to load new view")
            time.sleep(2)
        except TimeoutException:
            print(
                "ACCEPTING LOCATION: Loading took too much time! Element probably not presented, so we continue.")
        except Exception as e:
            print("def login(self): 5: %s" % str(e))

    def denyOverlayedNotifications(self):
        try:
            xpath = '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]'
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))

            denyNotificationsBtn = self.browser.find_element_by_xpath(xpath)
            denyNotificationsBtn.click()
            print("DENIED NOTIFICATIONS")
            print("Sleeping 2 seconds to load new view")
            time.sleep(2)
        except TimeoutException:
            print(
                "DENYING NOTIFICATIONS: Loading took too much time! Element probably not presented, so we continue.")
        except Exception as e:
            print("def login(self): 6: %s" % str(e))

    def acceptCookies(self):
        try:
            xpath = '//*[@id="content"]/div/div[2]/div/div/div[1]/button'
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))

            acceptCookiesBtn = self.browser.find_element_by_xpath(xpath)
            acceptCookiesBtn.click()
            print("ACCEPTED COOKIES")
            print("Sleeping 2 seconds to load new view")
            time.sleep(2)
        except TimeoutException:
            print(
                "ACCEPTING COOKIES: Loading took too much time! Element probably not presented, so we continue.")
        except Exception as e:
            print("def login(self): 7: %s" % str(e))

    def denySeeWhoLikedYou(self):
        try:
            xpath = '//*[@id="modal-manager"]/div/div/div/div[3]/button[2]'

            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))

            denyBtn = self.browser.find_element_by_xpath(xpath)
            denyBtn.click()
            print("DENIED SEE WHO LIKED YOU")
            print("Sleeping 2 seconds to load new view")
            time.sleep(2)
        except TimeoutException:
            print(
                "DENYING SEE WHO LIKES YOU: Loading took too much time! Element probably not presented, so we continue.")
        except Exception as e:
            print("def login(self): 8: %s" % str(e))

    def changeFocusToPopUp(self):
        max_tries = 50
        current_tries = 0

        main_window = None
        while not main_window and current_tries < max_tries:
            current_tries += 1
            main_window = self.browser.current_window_handle

        current_tries = 0
        popup_window = None
        while not popup_window:
            current_tries += 1

            if current_tries >= max_tries:
                print("tries exceeded")
                return False

            for handle in self.browser.window_handles:
                if handle != main_window:
                    popup_window = handle
                    break

        self.browser.switch_to.window(popup_window)
        return True

    def changeFocusToMainWindow(self):
        main_window = None
        if len(self.browser.window_handles) == 1:
            main_window = self.browser.current_window_handle
        else:
            popup_window = self.browser.current_window_handle
            while not main_window:
                for handle in self.browser.window_handles:
                    if handle != popup_window:
                        main_window = handle
                        break

        self.browser.switch_to.window(main_window)