from pprint import pprint

from selenium import webdriver

from action import constants
from action.config import parse_config
from action.login import login_sequence
from screen.resource import ResourceGenericScreen


def launch_bot():
    username, password, url = parse_config()

    driver = webdriver.Firefox()
    try:
        driver.get(url)
        print("Loaded page.")

        login_sequence(driver, username, password)
        with ResourceGenericScreen(driver) as resource_tab:
            pprint(resource_tab.extract_info())

        input("Waiting...")
    finally:
        driver.quit()


if __name__ == "__main__":
    launch_bot()
