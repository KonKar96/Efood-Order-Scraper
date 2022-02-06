from enum import unique
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common import exceptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import json
import pickle
import requests
import discord
import textwrap
import datetime
import csv
import math

EMAIL = ""
PASSWORD = ""


def sleep(x):
    print(
        "------------------------------------------------------- \n                    sleeping for"
    )
    for i in range(x, 0, -1):
        sys.stdout.write(str(i) + " ")
        sys.stdout.flush()
        time.sleep(1)
    print(
        "\n------------------------------------------------------- \n                    waking up"
    )


def find(xpath, mode=None):
    tries = 0
    while True:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            if mode == "click":
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
            element.location_once_scrolled_into_view
            return element
        except (
            exceptions.StaleElementReferenceException,
            exceptions.ElementClickInterceptedException,
            exceptions.ElementNotInteractableException,
            exceptions.TimeoutException,
            AttributeError,
            UnboundLocalError,
        ):
            tries += 1
            if tries > 10:
                return None
            pass


def telegram_bot_sendtext(bot_message):
    bot_token = "871715863:AAGynJz0g8IT3bDKZZBtnXLL35ojVj0z6iA"
    bot_chatID = "787048928"
    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + bot_chatID
        + "&parse_mode=Markdown&text="
        + bot_message
    )
    response = requests.get(send_text)
    return response.json()


def login(driver):
    driver.get("https://www.e-food.gr/")
    find("//button[contains(text(),'Αποδοχή Όλων')]", "click").click()
    find("//button[@data-event='Header Login']").click()
    find("//input[@id='login_email']").send_keys(EMAIL)
    find("//input[@id='login_password']").send_keys(PASSWORD)
    find("//button[contains(text(),'Κάνε σύνδεση')]").click()
    if find("//div/strong") is not None:
        print("Login successful")
    else:
        print("Login failed")
        login(driver)
    return


def logout(driver):
    find("//div/strong").click()
    find(
        "//li[@class='user-options-list-item site-header-user-options-list-item-logout border-top']"
    ).click()
    print("Logged out")


def get_orders(driver):
    driver.get("https://www.e-food.gr/account/orders")
    find("//div[@class='col-6 col-lg-2 mb-7 mb-lg-0'][1]/strong")

    after_click = []
    while True:
        before_click = driver.find_elements(
            By.XPATH, "//div[@class='col-6 col-lg-2 mb-7 mb-lg-0'][1]/strong"
        )
        try:
            WebDriverWait(driver, 0.5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@id='load-more-orders']")
                )
            )
            if len(after_click) != len(before_click):
                after_click = before_click
                print("Found more orders")
                find("//button[@id='load-more-orders']").click()
        except Exception:
            print("No more orders")
            break

    ids = []
    prices = []

    for row in find("//ul[@class='list-unstyled']").text.split("\n"):
        if row.isdigit() and len(row) >= 5:
            ids.append(row)
        if "€" in row and "," in row:
            try:
                float(row.replace("€", "").replace(",", "."))
                prices.append(float(row.replace("€", "").replace(",", ".")))
            except ValueError:
                continue

    # print("Found " + str(len(ids)) + " orders")
    max_val = max(prices)
    print(
        f"""Total Orders: {str(len(prices))}
Total Spent: {str(sum(prices))}
Order ID: {ids[prices.index(max_val)]} has the highest price of {max_val}
    """
    )


def efood(driver):
    begin_time = datetime.datetime.now()
    login(driver)
    get_orders(driver)
    print(f"Script Total Time: {datetime.datetime.now() - begin_time}")
    logout(driver)
    return


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1020,720")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    efood(driver)
    driver.close()
