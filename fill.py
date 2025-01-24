import argparse
import datetime
from getpass import getpass
import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://vtportal.visualtime.net/2/indexv2.aspx#home")

    sleep(2.5)

    return driver


def login(driver, email, password):

    print("opening client id input and writing the server")
    sleep(1)
    action_chains = ActionChains(driver)
    action_chains.send_keys(Keys.TAB).pause(1).send_keys(Keys.TAB).pause(0.5).send_keys("aeti6951").pause(
        0.5
    ).send_keys(Keys.TAB).pause(0.5).send_keys(Keys.ENTER).perform()
    sleep(1)

    print("clicking the login with SSO")
    # the last "get-to-work-blue" is the SSO login
    submit = driver.find_elements(By.CLASS_NAME, "get-to-work-blue")[-1]
    submit.send_keys(Keys.ENTER)
    print("opening Okta form...")
    sleep(10)  # long time until okta form loads

    print("filling okta email")
    action_chains = ActionChains(driver)
    action_chains.send_keys(email).send_keys(Keys.TAB).pause(0.5).send_keys(Keys.SPACE).pause(0.5).send_keys(
        Keys.TAB
    ).pause(0.5).send_keys(Keys.ENTER).perform()
    sleep(2.5)

    print("filling okta password")
    action_chains = ActionChains(driver)
    action_chains.send_keys(password).send_keys(Keys.TAB).pause(0.5).send_keys(Keys.ENTER).perform()
    sleep(2.5)

    print("asking okta push notification")
    action_chains = ActionChains(driver)
    action_chains.send_keys(password).send_keys(Keys.TAB).pause(0.5).send_keys(Keys.TAB).pause(0.5).send_keys(
        Keys.ENTER
    ).perform()


def parse_dates(date_from, date_to):
    date_from_obj = datetime.datetime.strptime(date_from, "%Y-%m-%d")
    date_to_obj = datetime.datetime.strptime(date_to, "%Y-%m-%d")
    day_delta = datetime.timedelta(days=1)
    dates = []
    next_day = date_from_obj
    while next_day <= date_to_obj:
        if next_day.weekday() < 5:  # between monday and friday
            dates.append(next_day.strftime("%Y-%m-%d"))
        next_day += day_delta

    return dates


def submit_dates(driver, dates):
    def open_gestion_horaria(date):
        print("opening 'gestion horaria the first time'")

        print("opening hamburguer menu")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "tabMain")))
        sleep(3)
        driver.find_element(By.ID, "tabMain").click()
        sleep(2)

        print("clicking 'Gestion horaria'")
        driver.find_elements(By.CLASS_NAME, "dx-treeview-item")[2].click()
        sleep(2)

        date_id = date.replace("-", "")
        driver.find_element(By.ID, date_id).click()
        driver.find_element(By.ID, "listCalendarTemplate").click()
        print("now all set, we can start switching day by day throught the url")
        sleep(1)

    for date in dates:
        print(f"STARTING submit date {date}, start and end")

        print("START submit start")
        open_gestion_horaria(date)
        sleep(2)
        driver.find_element(By.ID, "btnActionMenuPopover").click()
        sleep(2)

        print("  open datepicker...")
        date_elem = driver.find_elements(By.CLASS_NAME, "dx-dropdowneditor-input-wrapper")[0]
        date_elem.click()
        sleep(0.5)

        print("  salecting start hour 9...")
        hour_div = driver.find_element(By.CLASS_NAME, "dx-dateviewroller-hours")
        sel = hour_div.find_element(By.CLASS_NAME, "dx-dateview-item-selected")
        drag = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(sel))
        ActionChains(driver).drag_and_drop_by_offset(drag, 0, -(36 * 9)).perform()  # 36 is the height in px
        sleep(0.5)

        print("  accepting time...")
        buttons = driver.find_elements(By.CLASS_NAME, "dx-button-text")
        buttons[-1].click()
        sleep(0.2)

        print("FINISHED submitting start time")
        save_button = driver.find_elements(By.CLASS_NAME, "mainMenuButton")[-1]
        save_button.click()
        sleep(2)

        print("START submit exit")
        open_gestion_horaria(date)
        sleep(2)
        driver.find_element(By.ID, "btnActionMenuPopover").click()
        sleep(2)

        print("  open datepicker...")
        date_elem = driver.find_elements(By.CLASS_NAME, "dx-dropdowneditor-input-wrapper")[0]
        date_elem.click()
        sleep(0.5)

        print("  salecting end hour 18...")
        hour_div = driver.find_element(By.CLASS_NAME, "dx-dateviewroller-hours")
        sel = hour_div.find_element(By.CLASS_NAME, "dx-dateview-item-selected")
        drag = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(sel))
        ActionChains(driver).drag_and_drop_by_offset(drag, 0, -(36 * 9)).perform()
        sel = hour_div.find_element(By.CLASS_NAME, "dx-dateview-item-selected")
        drag = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(sel))
        ActionChains(driver).drag_and_drop_by_offset(drag, 0, -(36 * 9)).perform()
        sleep(0.5)

        minutes = random.randint(1, 8)
        min_div = driver.find_element(By.CLASS_NAME, "dx-dateviewroller-minutes")
        sel = min_div.find_element(By.CLASS_NAME, "dx-dateview-item-selected")
        drag = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(sel))
        ActionChains(driver).drag_and_drop_by_offset(drag, 0, -(36 * minutes)).perform()
        min_div = driver.find_element(By.CLASS_NAME, "dx-dateviewroller-minutes")
        sel = min_div.find_element(By.CLASS_NAME, "dx-dateview-item-selected")
        drag = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(sel))
        ActionChains(driver).drag_and_drop_by_offset(drag, 0, -(36 * minutes)).perform()
        sleep(0.5)

        print("  accepting time...")
        buttons = driver.find_elements(By.CLASS_NAME, "dx-button-text")
        buttons[-1].click()
        sleep(0.2)

        print("  setting type 'salida'...")
        driver.find_elements(By.CLASS_NAME, "dx-texteditor-container")[2].click()
        driver.find_elements(By.CLASS_NAME, "dx-list-item")[-1].click()
        sleep(0.2)

        print("FINISHED submitting END time")
        save_button = driver.find_elements(By.CLASS_NAME, "mainMenuButton")[-1]
        save_button.click()
        sleep(1)


def fill(date_from, date_to, email, password):
    driver = setup()

    login(driver, email, password)

    dates = parse_dates(date_from, date_to)

    submit_dates(driver, dates)

    print("closing")
    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("date_from", help="yyyy-mm-dd")
    parser.add_argument("date_to", help="yyyy-mm-dd")
    parser.add_argument("email")
    args = parser.parse_args()
    password = getpass()
    fill(args.date_from, args.date_to, args.email, password)
