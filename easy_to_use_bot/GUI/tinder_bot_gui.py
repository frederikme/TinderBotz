#!/usr/bin/env python3

import threading
import subprocess
import customtkinter
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options as opt
import random, time, sys
from datetime import datetime


def get_bot():
    juba = opt()

    # enter your chrome profile path 
    juba.add_argument('--profile-directory=')
    juba.add_argument('--user-data-dir=')

    global driver
    driver = uc.Chrome(options=juba) 
    time.sleep(3)
    # Navigate to url
    driver.get("https://tinder.com/app/recs")
    # Here I wating until you log into your account in case you have to log in or something ( I know it's a bit weird but it works )
    wait = WebDriverWait(driver, 100000000)
    like_button = "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[4]/button" 
    wait.until(EC.visibility_of_element_located((By.XPATH, like_button)))

    global active_element 
    active_element = driver.switch_to.active_element


def dismiss_alert(driver):
    """Handle any pop-up if any"""
    # Deny confirmation of email
    try:
        xpath = './/main/div/div[1]/div[2]/button[2]'
        remindmelater = driver.find_element(By.XPATH, xpath)
        remindmelater.click()
        time.sleep(3)
    except NoSuchElementException:
        pass

    # Deny add location popup
    try:
        xpath = ".//*[contains(text(), 'No Thanks')]"
        nothanks = driver.find_element(By.XPATH, xpath)
        nothanks.click()
        time.sleep(3)
    except NoSuchElementException:
        pass

    try:
        driver.switch_to.alert.dismiss()
    except:
        pass

    try:
        box = driver.find_element(By.XPATH, '//button/span[text()="Maybe Later" or text()="Not interested" or text()="No Thanks"]')
        box.click()
    except NoSuchElementException:
        pass

    try:
        driver.refresh()
    except:
        pass 


def intercart(active_element):
    """Show the bio"""
    active_element.send_keys(Keys.ARROW_UP)
    time.sleep(2)
    active_element.send_keys(Keys.ARROW_DOWN)


def go_through_picutre(active_element):
    for i in range(3):
        active_element.send_keys(Keys.SPACE)
        time.sleep(1)


def swipe(active_element):
    """Swipe just like a human"""
    button = [Keys.RIGHT, Keys.LEFT]
    random_button = random.choice(button)
    active_element.send_keys(random_button)
    time.sleep(2)


def close_match(driver):
    """Send a random custom message if a match is found"""
    try:
        close_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/main/div[2]/main/div/div[1]/div/div[4]/button")
        close_button.click()
    except NoSuchElementException:
        pass


def run_bot():
    """Run the bot for a specified number of swipes"""
    get_bot()
    for i in range(1000):
        try:
            intercart(active_element)
            go_through_picutre(active_element)
            swipe(active_element)
            try:
                close_match(driver)
            except:
                pass
        except:
            dismiss_alert(driver)


def start_bot():
    # Create a new thread to run the bot
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()


def close_it():
    sys.exit()


# ------------------------- > the GUI

app = customtkinter.CTk()
app.title("Bots")
app.geometry("500x300")
app.grid_columnconfigure((0), weight=1)


def combobox_callback(choice):
    pass


combobox_apps = customtkinter.CTkComboBox(
    app,
    values=["Tinder"],
    command=combobox_callback,
    width=400,
    height=50,
    font=("Arial", 20, "bold"),
    dropdown_font=("Arial", 20, "bold"),
    hover=True,
    justify="center",
    corner_radius=10
)


button_start = customtkinter.CTkButton(
    app,
    text="Start",
    command=start_bot,
    width=100,
    height=30,
    corner_radius=8,
    hover_color="gray",
    hover=True,
    font=("Arial", 20, "bold"),
)

button_stop = customtkinter.CTkButton(
    app,
    text="Stop",
    command=close_it,
    width=100,
    height=30,
    corner_radius=8,
    hover_color="gray",
    hover=True,
    font=("Arial", 20, "bold"),
)

# --------------------------> packing

combobox_apps.grid(row=1, column=0, padx=10, pady=40, sticky="nsew", columnspan=2)

button_start.grid(row=4, column=0, padx=10, pady=40, sticky="nsew")
button_stop.grid(row=4, column=1, padx=10, pady=40, sticky="nsew")

app.mainloop()

