from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time


class LoginHelper:

    delay = 5

    def __init__(self, browser):
        self.browser = browser

    def clickLoginButton(self):
        try:
            xpath = '//*[@type="button"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))
            buttons = self.browser.find_elements_by_xpath(xpath)

            for button in buttons:
                text_span = button.find_element_by_xpath('.//span').text
                if 'log in' in text_span.lower():
                    button.click()
                    break

        except TimeoutException:
            self.exitByTimeOut()

        except ElementClickInterceptedException:
            pass

    def loginByGoogle(self, email, password):
        self.clickLoginButton()

        # wait for google button to appear
        try:
            xpath = '//*[@aria-label="Log in with Google"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            btn = self.browser.find_element_by_xpath(xpath)
            time.sleep(2)
            btn.click()

        except TimeoutException:
            self.exitByTimeOut()

        if not self.changeFocusToPopUp():
            print("FAILED TO CHANGE FOCUS TO POPUP")
            print("Let's try again...")
            return self.loginByGoogle(email, password)

        try:
            xpath = "//input[@type='email']"
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))

            emailfield = self.browser.find_element_by_xpath(xpath)
            emailfield.send_keys(email)
            emailfield.send_keys(Keys.ENTER)
            # sleeping 3 seconds for passwordfield to come through
            time.sleep(3)
        except TimeoutException:
            self.exitByTimeOut()

        try:
            xpath = "//input[@type='password']"
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))

            pwdfield = self.browser.find_element_by_xpath(xpath)
            pwdfield.send_keys(password)
            pwdfield.send_keys(Keys.ENTER)

        except TimeoutException:
            self.exitByTimeOut()

        self.changeFocusToMainWindow()
        self.handlePopups()

    def loginByFacebook(self, email, password):
        self.clickLoginButton()

        # wait for facebook button to appear
        try:
            xpath = '//*[@aria-label="Login with Facebook"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            btn = self.browser.find_element_by_xpath(xpath)
            time.sleep(2)
            btn.click()
        except TimeoutException:
            self.exitByTimeOut()

        if not self.changeFocusToPopUp():
            print("FAILED TO CHANGE FOCUS TO POPUP")
            print("Let's try again...")
            return self.loginByFacebook(email, password)

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

        except TimeoutException:
            self.exitByTimeOut()

        self.changeFocusToMainWindow()
        self.handlePopups()

    def handlePopups(self):
        time.sleep(2)
        self.acceptCookies()
        self.acceptLocationNotification()
        self.denyOverlayedNotifications()

    def acceptLocationNotification(self):
        try:
            xpath = '//*[@data-testid="allow"]'#'//*[@aria-label="Allow"]'
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))

            locationBtn = self.browser.find_element_by_xpath(xpath)
            locationBtn.click()
            print("ACCEPTED LOCATION.")
        except TimeoutException:
            print(
                "ACCEPTING LOCATION: Loading took too much time! Element probably not presented, so we continue.")
        except:
            pass

    def denyOverlayedNotifications(self):
        try:
            xpath = '//*[@data-testid="decline"]'
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))

            self.browser.find_element_by_xpath(xpath).click()
            print("DENIED NOTIFICATIONS.")
        except TimeoutException:
            print(
                "DENYING NOTIFICATIONS: Loading took too much time! Element probably not presented, so we continue.")
        except:
            pass

    def acceptCookies(self):
        try:
            xpath = '//*[@type="button"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))
            buttons = self.browser.find_elements_by_xpath(xpath)

            for button in buttons:
                text_span = button.find_element_by_xpath('.//span').text
                if 'i accept' in text_span.lower():
                    button.click()
                    break
            print("COOKIES ACCEPTED.")
        except TimeoutException:
            print(
                "ACCEPTING COOKIES: Loading took too much time! Element probably not presented, so we continue.")
        except:
            pass

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
            time.sleep(0.30)
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

    def exitByTimeOut(self):
        print("Loading took an element too much time!. Please check your internet connection.")
        print("Alternatively, you can add a sleep or higher the delay class variable.")
        exit(1)