from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time


class LoginHelper:

    delay = 7

    def __init__(self, browser):
        self.browser = browser
        self.acceptCookies()

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
            xpath = '//*[@aria-label="Log in with Facebook"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            self.browser.find_element_by_xpath(xpath).click()
        except TimeoutException:
            self.exitByTimeOut()

        if not self.changeFocusToPopUp():
            print("FAILED TO CHANGE FOCUS TO POPUP")
            print("Let's try again...")
            return self.loginByFacebook(email, password)

        try:
            xpath_email = '//*[@id="email"]'
            xpath_password = '//*[@id="pass"]'
            xpath_button = '//*[@id="loginbutton"]'

            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath_email)))

            emailfield = self.browser.find_element_by_xpath(xpath_email)
            emailfield.send_keys(email)

            pwdfield = self.browser.find_element_by_xpath(xpath_password)
            pwdfield.send_keys(password)

            loginbutton = self.browser.find_element_by_xpath(xpath_button)
            loginbutton.click()

        except TimeoutException:
            self.exitByTimeOut()

        self.changeFocusToMainWindow()
        self.handlePopups()

    def loginBySMS(self, country, phone_number):
        self.clickLoginButton()

        # wait for facebook button to appear
        try:
            xpath = '//*[@aria-label="Log in with phone number"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            btn = self.browser.find_element_by_xpath(xpath)
            btn.click()
        except TimeoutException:
            self.exitByTimeOut()

        self.handlePrefix(country)

        # Fill in sms
        try:
            xpath = '//*[@name="phone_number"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

            field = self.browser.find_element_by_xpath(xpath)
            field.send_keys(phone_number)
            field.send_keys(Keys.ENTER)

        except TimeoutException:
            self.exitByTimeOut()

        print("\n\nPROCEED MANUALLY BY ENTERING SMS CODE\n")
        # check every second if user has bypassed sms-code barrier
        while not self.isLoggedIn():
            time.sleep(1)

        self.handlePopups()

    def handlePrefix(self, country):
        self.acceptCookies()

        xpath = '//div[@aria-describedby="phoneErrorMessage"]/div/div'
        WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
            (By.XPATH, xpath)))
        btn = self.browser.find_element_by_xpath(xpath)
        btn.click()

        els = self.browser.find_elements_by_xpath('//div')
        for el in els:
            try:
                span = el.find_element_by_xpath('.//span')
                if span.text.lower() == country.lower():
                    print("clicked")
                    el.click()
                    break
                else:
                    print(span.text)
            except:
                continue

    # checks if user is logged in by checking the url
    def isLoggedIn(self):
        return 'app' in self.browser.current_url

    def handlePopups(self):
        time.sleep(2)
        self.acceptCookies()
        self.acceptLocationNotification()
        self.denyOverlayedNotifications()

    def acceptLocationNotification(self):
        try:
            xpath = '//*[@data-testid="allow"]'
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
        print("Loading an element took too much time!. Please check your internet connection.")
        print("Alternatively, you can add a sleep or higher the delay class variable.")
        exit(1)
