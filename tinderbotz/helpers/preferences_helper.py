from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from tinderbotz.helpers.constants_helper import Sexuality
import time

class PreferencesHelper:

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

    def set_distance_range(self, km):
        # correct out of bounds values
        if km > 160:
            final_percentage = 100
        elif km < 2:
            final_percentage = 0
        else:
            final_percentage = (km / 160) * 100

        possible_xpaths = ['//*[@aria-label="Maximum distance in kilometres"]',
                           '//*[@aria-label="Maximum distance in kilometers"]',
                           '//*[@aria-label="Maximum distance in miles"]']

        for xpath in possible_xpaths:
            try:
                WebDriverWait(self.browser, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                link = self.browser.find_element(By.XPATH, xpath)
                break
            except TimeoutException:
                continue

        print("\nSlider of distance will be adjusted...")
        current_percentage = float(link.get_attribute('style').split(' ')[1].split('%')[0])
        print("from {}% = {}km".format(current_percentage, current_percentage*1.6))
        print("to {}% = {}km".format(final_percentage, final_percentage*1.6))
        print("with a fault margin of 1%\n")

        # start adjusting the distance slider
        while abs(final_percentage - current_percentage) > 1:
            ac = ActionChains(self.browser)
            if current_percentage < final_percentage:
                ac.click_and_hold(link).move_by_offset(3, 0).release(link).perform()
            elif current_percentage > final_percentage:
                ac.click_and_hold(link).move_by_offset(-3, 0).release(link).perform()
            # update current percentage
            current_percentage = float(link.get_attribute('style').split(' ')[1].split('%')[0])

        print("Ended slider with {}% = {}km\n\n".format(current_percentage, current_percentage*1.6))
        time.sleep(5)

    def set_age_range(self, min, max):
        # locate elements
        xpath = '//*[@aria-label="Minimum age"]'
        WebDriverWait(self.browser, self.delay).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        btn_minage = self.browser.find_element(By.XPATH, xpath)

        xpath = '//*[@aria-label="Maximum age"]'
        WebDriverWait(self.browser, self.delay).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        btn_maxage = self.browser.find_element(By.XPATH, xpath)

        min_age_tinder = int(btn_maxage.get_attribute('aria-valuemin'))
        max_age_tinder = int(btn_maxage.get_attribute('aria-valuemax'))

        # correct out of bounds values
        if min < min_age_tinder:
            min = min_age_tinder

        if max > max_age_tinder:
            max = max_age_tinder

        while max-min < 5:
            max += 1
            min -= 1

            if min < min_age_tinder:
                min = min_age_tinder
            if max > max_age_tinder:
                max = max_age_tinder

        range_ages_tinder = max_age_tinder - min_age_tinder
        percentage_per_year = 100 / range_ages_tinder

        to_percentage_min = (min - min_age_tinder) * percentage_per_year
        to_percentage_max = (max - min_age_tinder) * percentage_per_year

        current_percentage_min = float(btn_minage.get_attribute('style').split(' ')[1].split('%')[0])
        current_percentage_max = float(btn_maxage.get_attribute('style').split(' ')[1].split('%')[0])

        print("\nSlider of ages will be adjusted...")
        print("Minimum age will go ...")
        print("from {}% = {} years old".format(current_percentage_min,
                                               (current_percentage_min/percentage_per_year)+min_age_tinder))
        print("to {}% = {} years old".format(to_percentage_min, min))
        print("Maximum age will go ...")
        print("from {}% = {} years old".format(current_percentage_max,
                                               (current_percentage_max / percentage_per_year) + min_age_tinder))
        print("to {}% = {} years old".format(to_percentage_max, max))
        print("with a fault margin of 1%\n")

        # start adjusting the distance slider
        while abs(to_percentage_min - current_percentage_min) > 1 or abs(to_percentage_max - current_percentage_max) > 1:
            ac = ActionChains(self.browser)

            if current_percentage_min < to_percentage_min:
                ac.click_and_hold(btn_minage).move_by_offset(5, 0).release(btn_minage).perform()
            elif current_percentage_min > to_percentage_min:
                ac.click_and_hold(btn_minage).move_by_offset(-5, 0).release(btn_minage).perform()

            ac = ActionChains(self.browser)
            if current_percentage_max < to_percentage_max:
                ac.click_and_hold(btn_maxage).move_by_offset(5, 0).release(btn_maxage).perform()
            elif current_percentage_max > to_percentage_max:
                ac.click_and_hold(btn_maxage).move_by_offset(-5, 0).release(btn_maxage).perform()

            # update current percentage
            current_percentage_min = float(btn_minage.get_attribute('style').split(' ')[1].split('%')[0])
            current_percentage_max = float(btn_maxage.get_attribute('style').split(' ')[1].split('%')[0])

        print("Ended slider with ages from {} years old  to {} years old\n\n".format((current_percentage_min/percentage_per_year)+min_age_tinder,
              (current_percentage_max / percentage_per_year) + min_age_tinder))
        time.sleep(5)

    def set_sexualitiy(self, type):
        if not isinstance(type, Sexuality):
            assert False

        xpath = '//*[@href="/app/settings/gender"]/div/div/div/div'
        WebDriverWait(self.browser, self.delay).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        element = self.browser.find_element(By.XPATH, xpath)
        element.click()

        xpath = '//*[@aria-pressed="false"]'.format(type.value)
        WebDriverWait(self.browser, self.delay).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        elements = self.browser.find_elements(By.XPATH, xpath)

        for element in elements:
            if element.find_element(By.XPATH, './/div/label').text == type.value:
                element.click()
                break

        print("clicked on " + type.value)
        time.sleep(5)

    def set_global(self, boolean, language=None):
        # check if global is already activated
        # Global is activated when the href to preferred languages is visible
        is_activated = False
        try:
            xpath = '//*[@href="/app/settings/global/languages"]/div'
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            self.browser.find_element(By.XPATH, xpath)
            is_activated = True

        except:
            pass

        if boolean != is_activated:
            xpath = '//*[@name="global"]'
            element = self.browser.find_element(By.XPATH, xpath)
            element.click()

        if is_activated and language:
            print("\nUnfortunately, Languages setting feature does not yet exist")
            print("If needed anyways:\nfeel free to open an issue and ask for the feature")
            print("or contribute by making a pull request.\n")

            '''
            languages_element.click()
            xpath = "//*[contains(text(), {})]".format(language)
            WebDriverWait(self.browser, self.delay).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            self.browser.find_elements(By.XPATH, xpath).click()
            '''
            time.sleep(5)
