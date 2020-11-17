from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


class ProfileHelper:

    delay = 5

    HOME_URL = "https://www.tinder.com/app/recs"

    def __init__(self, browser):
        self.browser = browser
        if self.HOME_URL is not self.browser.current_url:
            self.browser.get(self.HOME_URL)

        # open profile
        try:
            xpath = '//*[@href="/app/profile"]'
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            browser.find_element_by_xpath(xpath).click()
        except TimeoutException:
            print("Make sure user is logged in before changing settings in profile!")
            assert False

    def setDistanceRadius(self, km):
        # correct out of bounds values
        if km > 160:
            final_percentage = 100
        elif km < 2:
            final_percentage = 1
        else:
            final_percentage = (km / 160) * 100

        try:
            xpath = '//*[@aria-label="Maximum distance in kilometres"]'
            WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            link = self.browser.find_element_by_xpath(xpath)
        except TimeoutException:
            # element not found in time, so let's try the american metric system
                xpath = '//*[@aria-label="Maximum distance in miles"]'
                link = self.browser.find_element_by_xpath(xpath)

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
