from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from tinderbotz.helpers.xpaths import content, modal_manager
from selenium.webdriver.common.keys import Keys

import time, os

class ProfileHelper:

    delay = 5

    HOME_URL = "https://www.tinder.com/app/profile"

    def __init__(self, browser):
        self.browser = browser

        # open profile
        try:
            xpath = '//*[@href="/app/profile"]'
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            browser.find_element(By.XPATH, xpath).click()
        except:
            pass

        self._edit_info()

    def _edit_info(self):
        xpath = '//a[@href="/app/profile/edit"]'

        try:
            WebDriverWait(self.browser, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            self.browser.find_element(By.XPATH, xpath).click()
            time.sleep(1)
        except Exception as e:
            print(e)

    def _save(self):
        xpath = f"{content}/div/div[1]/div/main/div[1]/div/div/div/div/div[1]/a"
        try:
            WebDriverWait(self.browser, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            self.browser.find_element(By.XPATH, xpath).click()
            time.sleep(1)
        except Exception as e:
            print(e)

    def add_photo(self, filepath):
        # get the absolute filepath instead of the relative one
        filepath = os.path.abspath(filepath)

        # "add media" button
        xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div/div/div[2]/span/button'
        try:
            WebDriverWait(self.browser, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            btn = self.browser.find_element(By.XPATH, xpath)
            self.browser.execute_script("arguments[0].scrollIntoView();", btn)
            btn.click()
        except Exception as e:
            print(e)

        xpath_input = f"{modal_manager}/div/div/div[1]/div[2]/div[2]/div/div/input"
        try:
            WebDriverWait(self.browser, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, xpath_input)))
            self.browser.find_element(By.XPATH, xpath_input).send_keys(filepath)
        except Exception as e:
            print(e)

        xpath_choose = f"{modal_manager}/div/div/div[1]/div[1]/button[2]"
        try:
            WebDriverWait(self.browser, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, xpath_choose)))
            self.browser.find_element(By.XPATH, xpath_choose).click()
        except Exception as e:
            print(e)

        self._save()

    def set_bio(self, bio):
        xpath = f"{content}/div/div[1]/div/main/div[1]/div/div/div/div/div[2]/div[2]/div/textarea"

        try:
            WebDriverWait(self.browser, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            text_area = self.browser.find_element(By.XPATH, xpath)

            for _ in range(500):
                text_area.send_keys(Keys.BACKSPACE)

            time.sleep(1)
            text_area.send_keys(bio)
            time.sleep(1)
        except Exception as e:
            print(e)

        self._save()
