import os
import sys
from contextlib import contextmanager

import numpy as np
from selenium import webdriver
from selenium.common import exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PATH = "chromedriver.exe"
email = "Enter efood account mail"
password = "Enter efood account password"
euroSign = "€"
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
# options.add_argument('--headless')
options.add_argument("--disable-gpu")
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(PATH, options=options)
loginStateFirstAttempt = True


def findByXpathLoop(xpath):
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
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
        findByXpathLoop(xpath)


def loginFacebook(loginStateFirstAttempt):
    if loginStateFirstAttempt is True:
        loginFacebookButton = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='login-form']/div[1]/div[1]/button[1]")
            )
        )
        ActionChains(driver).click(loginFacebookButton).perform()
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        loginStateFirstAttempt = False

    loginEmailSection = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='email']"))
    )
    loginEmailSection.send_keys("enter google account email here")

    loginPasswordSection = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='pass']"))
    )
    loginPasswordSection.send_keys("enter google account password here")
    loginPasswordSection.send_keys(Keys.RETURN)

    loginFacebookError = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='error_box']"))
    )
    if loginFacebookError:
        loginFacebook(loginStateFirstAttempt)


def loginGoogle(loginStateFirstAttempt):
    loginGoogleButton = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@id='login-form']/div[1]/div[2]/button")
        )
    )
    ActionChains(driver).click(loginGoogleButton).perform()
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)

    loginEmailSection = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='identifierId']"))
    )

    loginEmailSection.send_keys("enter google account email here")
    loginEmailSection.send_keys(Keys.RETURN)

    loginPasswordSection = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
    )

    loginPasswordSection.send_keys("enter google account password here")
    loginPasswordSection.send_keys(Keys.RETURN)

    WebDriverWait(driver, 1000).until(
        EC.invisibility_of_element_located(
            (By.XPATH, "//figure[@data-illustration='authzenDefault']")
        )
    )


def loginEfood(loginStateFirstAttempt):
    if loginStateFirstAttempt is True:
        loginStateFirstAttempt = False

    loginEmailSection = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='login_email']"))
    )
    loginPasswordSection = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='pass']"))
    )

    loginEmailSection.clear()
    loginPasswordSection.clear()

    loginEmailSection.send_keys(email)
    loginPasswordSection.send_keys(password)

    loginPasswordSection.send_keys(Keys.RETURN)


def loginButtons(window_before):
    try:
        loginButton = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@data-target='#myModal']/strong")
            )
        )
        loginButton.click()
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//strong[@class='h2']"))
        )
        WebDriverWait(driver, 100).until(
            EC.invisibility_of_element_located((By.XPATH, "/div[@id='ef-loader']"))
        )
        print("Efood account - 1\n")
        print("Facebook account - 2\n")
        print("Google account - 3\n")
        loginChoice = input("....")
        if loginChoice == str(1):
            loginEfood(loginStateFirstAttempt)
            return
        elif loginChoice == str(2):
            loginFacebook(loginStateFirstAttempt)
            driver.switch_to.window(window_before)
            return
        elif loginChoice == str(3):
            loginGoogle(loginStateFirstAttempt)
            driver.switch_to.window(window_before)
            return
        else:
            print("pathse kapoio apo to 1-3:")
    except (
        exceptions.StaleElementReferenceException,
        exceptions.ElementClickInterceptedException,
        exceptions.ElementNotInteractableException,
        exceptions.TimeoutException,
        AttributeError,
        UnboundLocalError,
        NoSuchElementException,
    ):
        driver.get("https://www.e-food.gr/account/orders")
        loginButtons(window_before)


def getOrders():
    driver.get("https://www.e-food.gr/")
    window_before = driver.window_handles[0]

    loginButtons(window_before)

    greeting = (
        WebDriverWait(driver, 100)
        .until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='row']/child::div[@class='col-lg-6']/div/child::div[@class='homepage-address-search-inner w-100 h-50 px-7 pt-7 pb-11 bg-white rounded mb-7 mb-lg-4 px-lg-0']/h1",
                )
            )
        )
        .text
    )
    print(greeting.replace("Πείνασες;", ""))

    driver.get("https://www.e-food.gr/account/orders")
    x = 0
    while True:
        try:
            orders = driver.find_elements_by_css_selector(
                ".p-7.px-lg-5.px-xl-9.border-bottom.user-account-orders-order"
            )
            if len(orders) > x:
                x = len(orders)
                showMore = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@id='load-more-orders']")
                    )
                )
                showMore.location_once_scrolled_into_view
                showMore.click()
            else:
                showMore = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@id='load-more-orders']")
                    )
                )
        except (
            exceptions.StaleElementReferenceException,
            exceptions.ElementClickInterceptedException,
            exceptions.ElementNotInteractableException,
            exceptions.TimeoutException,
            AttributeError,
            UnboundLocalError,
            NoSuchElementException,
        ):
            print("---------------------------------")
            break
    getStats(orders)


def getStats(orders):
    (
        ids,
        dates,
        times,
        restaurants,
        restaurantsLinks,
        description,
        costs,
        payMethods,
        years,
        months,
        days,
        hours,
    ) = ([], [], [], [], [], [], [], [], [], [], [], [])
    i, paidPayPal, paidCreditCard, paidCash = 0, 0, 0, 0

    for order in orders:
        if i == len(orders):
            break
        print(i)
        ids.append(
            order.find_element_by_css_selector("div>div:nth-child(1)>strong").text
        )
        dates.append(
            order.find_element_by_css_selector("div>div:nth-child(2)>strong").text
        )
        years.append(int("".join((list(dates[i]))[6:10])))
        months.append(int("".join((list(dates[i]))[3:5])))
        days.append(int("".join((list(dates[i]))[0:2])))

        times.append(
            order.find_element_by_css_selector("div>div:nth-child(2)>div>em").text
        )
        hours.append(int("".join((list(times[i]))[0:2])))

        restaurants.append(
            order.find_element_by_css_selector("div>div:nth-child(3)>div>a").text
        )
        restaurantsLinks.append(
            order.find_element_by_css_selector(
                "div>div:nth-child(3)>div>a"
            ).get_attribute("href")
        )
        description.append(
            order.find_element_by_css_selector("div>div:nth-child(4)>div").text
        )
        costs.append(
            float(
                order.find_element_by_css_selector("div>div:nth-child(5)>div")
                .text.replace("€", "")
                .replace(",", ".")
            )
        )
        try:
            if (
                order.find_element_by_css_selector(
                    "div>div:nth-child(5)>span>i"
                ).get_attribute("title")
                == "Πληρώσατε με PayPal"
            ):
                payMethods.append("PayPal")
                paidPayPal += 1
            elif (
                order.find_element_by_css_selector(
                    "div>div:nth-child(5)>span>i"
                ).get_attribute("title")
                == "Πληρώσατε με πιστωτική κάρτα"
            ):
                payMethods.append("CreditCard")
                paidCreditCard += 1
        except (
            exceptions.StaleElementReferenceException,
            exceptions.ElementClickInterceptedException,
            exceptions.ElementNotInteractableException,
            exceptions.TimeoutException,
            AttributeError,
            UnboundLocalError,
            NoSuchElementException,
        ):
            payMethods.append("Cash")
            paidCash += 1
        i += 1

    sum = np.sum(costs)
    avg = np.average(costs)
    print(str(sum) + ": Χρήματα που δαπανήθηκαν")
    print(str(len(orders)) + ": Συνολικές παραγγελίες")
    print(str(avg) + ": ΜΟ παραγγελίας")
    print("-YEARS-")
    unique, counts = np.unique(years, return_counts=True)
    print(dict(zip(unique, counts)))
    print("-MONTHS-")
    unique, counts = np.unique(months, return_counts=True)
    print(dict(zip(unique, counts)))
    print("-DAYS-")
    unique, counts = np.unique(days, return_counts=True)
    print(dict(zip(unique, counts)))
    print("-HOURS-")
    unique, counts = np.unique(hours, return_counts=True)
    print(dict(zip(unique, counts)))


if __name__ == "__main__":
    getOrders()
    driver.quit()
