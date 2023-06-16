#!/usr/bin/env python3

import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import undetected_chromedriver as uc

juba = ChromeOptions()
juba.add_argument('--profile-directory=')
juba.add_argument('--user-data-dir=')

driver = uc.Chrome(options=juba)
time.sleep(3)

# Navigate to URL
driver.get("https://tinder.com/app/recs")

wait = WebDriverWait(driver, 100000000)
like_button = "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[4]/button"
wait.until(EC.visibility_of_element_located((By.XPATH, like_button)))

active_element = driver.switch_to.active_element


def dismiss_alert():
    """Handle any pop-up if any"""
    try:
        xpath = './/main/div/div[1]/div[2]/button[2]'
        remindmelater = driver.find_element(By.XPATH, xpath)
        remindmelater.click()
        time.sleep(3)
    except:
        pass

    try:
        xpath = ".//*[contains(text(), 'No Thanks')]"
        nothanks = driver.find_element(By.XPATH, xpath)
        nothanks.click()
        time.sleep(3)
    except:
        pass

    try:
        driver.switch_to.alert.dismiss()
    except:
        pass

    try:
        box = driver.find_element(By.XPATH, '//button/span[text()="Maybe Later" or text()="Not interested" or text()="No Thanks"]')
        box.click()
    except:
        pass

    try:
        driver.refresh()
    except:
        pass


def intercart():
    """Try to show the bio or something for some reason I think that would be like human like behaviour """
    active_element.send_keys(Keys.ARROW_UP)
    time.sleep(2)
    active_element.send_keys(Keys.ARROW_DOWN)


def go_through_picture():
    for _ in range(3):
        active_element.send_keys(Keys.SPACE)
        time.sleep(1)


def swipe():
    """Swipe just like a human (Random stuff)"""
    buttons = [Keys.RIGHT, Keys.LEFT]
    random_button = random.choice(buttons)
    active_element.send_keys(random_button)
    time.sleep(2)


def send_message():
    """Send a random custom message if a match is found"""
    try:
        # Extract the match's name from the profile page
        name = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[2]/main/div/div[1]/div/div[3]/div[2]').text.split()[0]

        try:
            message_box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[2]/main/div/div[1]/div/div[3]/div[3]/form/textarea')
            message = f"Hey {name}"
            message_box.send_keys(message)
            time.sleep(3)
            message_box.send_keys(Keys.RETURN)
        except:
            message_box = driver.find_element(By.CSS_SELECTOR, '#s-1698539549')
            message = f"Hey {name}"
            message_box.send_keys(message)
            time.sleep(1)
            message_box.send_keys(Keys.RETURN)

    except:
        pass


def run_bot(num_swipes):
    """Run the bot for a specified number of swipes"""
    for _ in range(num_swipes):
        try:
            intercart()
            go_through_picture()
            swipe()
            try:
                send_message()
            except:
                pass
        except:
            dismiss_alert()


if __name__ == "__main__":
    run_bot(100)
    driver.quit()

