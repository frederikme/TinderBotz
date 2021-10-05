from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from tinderbotz.helpers.xpaths import content
import time

class LoginHelper:

    delay = 7

    def __init__(self, browser):
        self.browser = browser
        self._accept_cookies()

    def _click_login_button(self):
        try:
            xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))
            button = self.browser.find_element_by_xpath(xpath)
            button.click()
            time.sleep(3)

        except TimeoutException:
            self._exit_by_time_out()

        except ElementClickInterceptedException:
            pass

    def login_by_google(self, email, password):
        self._click_login_button()

        # wait for google button to appear
        xpath = '//*[@aria-label="Log in with Google"]'
        try:
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            self.browser.find_element_by_xpath(xpath).click()

        except TimeoutException:
            self._exit_by_time_out()
        except StaleElementReferenceException:
            # page was still loading when attempting to click facebook login
            time.sleep(4)
            self.browser.find_element_by_xpath(xpath).click()

        if not self._change_focus_to_pop_up():
            print("FAILED TO CHANGE FOCUS TO POPUP")
            print("Let's try again...")
            return self.login_by_google(email, password)

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
            self._exit_by_time_out()

        try:
            xpath = "//input[@type='password']"
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))

            pwdfield = self.browser.find_element_by_xpath(xpath)
            pwdfield.send_keys(password)
            pwdfield.send_keys(Keys.ENTER)

        except TimeoutException:
            self._exit_by_time_out()

        self._change_focus_to_main_window()
        self._handle_popups()

    def login_by_facebook(self, email, password):
        self._click_login_button()

        # wait for facebook button to appear
        xpath = '//*[@aria-label="Log in with Facebook"]'
        try:
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            self.browser.find_element_by_xpath(xpath).click()
        except TimeoutException:
            self._exit_by_time_out()
        except StaleElementReferenceException:
            # page was still loading when attempting to click facebook login
            time.sleep(4)
            self.browser.find_element_by_xpath(xpath).click()

        if not self._change_focus_to_pop_up():
            print("FAILED TO CHANGE FOCUS TO POPUP")
            print("Let's try again...")
            return self.login_by_facebook(email, password)

        try:
            xpath_cookies = '//*[@data-cookiebanner="accept_button"]'

            WebDriverWait(self.browser, self.delay).until(
            EC.presence_of_element_located((By.XPATH, xpath_cookies)))

            self.browser.find_element_by_xpath(xpath_cookies).click()
        except TimeoutException:
            # Not everyone might have the cookie banner so let's just continue then
            pass

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
            self._exit_by_time_out()

        self._change_focus_to_main_window()
        self._handle_popups()

    def login_by_sms(self, country, phone_number):
        self._click_login_button()

        # wait for facebook button to appear
        try:
            xpath = '//*[@aria-label="Log in with phone number"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            btn = self.browser.find_element_by_xpath(xpath)
            btn.click()
        except TimeoutException:
            self._exit_by_time_out()

        self._handle_prefix(country)

        # Fill in sms
        try:
            xpath = '//*[@name="phone_number"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

            field = self.browser.find_element_by_xpath(xpath)
            field.send_keys(phone_number)
            field.send_keys(Keys.ENTER)

        except TimeoutException:
            self._exit_by_time_out()

        print("\n\nPROCEED MANUALLY BY ENTERING SMS CODE\n")
        # check every second if user has bypassed sms-code barrier
        while not self._is_logged_in():
            time.sleep(1)

        self._handle_popups()

    def _handle_prefix(self, country):
        self._accept_cookies()

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
    def _is_logged_in(self):
        return 'app' in self.browser.current_url

    def _handle_popups(self):
        for _ in range(20):
            if not self._is_logged_in():
                time.sleep(1.2)
            else:
                break

        if not self._is_logged_in():
            print('Still not logged in ... ?')
            input('Proceed manually and press ENTER to continue\n')

        time.sleep(2)
        self._accept_cookies()
        self._accept_location_notification()
        self._deny_overlayed_notifications()

        self.browser.execute_cdp_cmd(
            "Browser.grantPermissions",
            {
                "origin": "https://www.tinder.com",
                "permissions": ["geolocation"]
            },
        )

        time.sleep(5)

    def _accept_location_notification(self):
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

    def _deny_overlayed_notifications(self):
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

    def _accept_cookies(self):
        try:
            xpath = '//*[@type="button"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))
            buttons = self.browser.find_elements_by_xpath(xpath)

            for button in buttons:
                try:
                    text_span = button.find_element_by_xpath('.//span').text
                    if 'accept' in text_span.lower():
                        button.click()
                        print("COOKIES ACCEPTED.")
                        break
                except NoSuchElementException:
                    pass

        except TimeoutException:
            print(
                "ACCEPTING COOKIES: Loading took too much time! Element probably not presented, so we continue.")
        except Exception as e:
            print("Error cookies", e)
            pass

    def _change_focus_to_pop_up(self):
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

    def _change_focus_to_main_window(self):
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

    def _exit_by_time_out(self):
        print("Loading an element took too much time!. Please check your internet connection.")
        print("Alternatively, you can add a sleep or higher the delay class variable.")
        exit(1)
