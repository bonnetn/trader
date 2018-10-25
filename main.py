from pprint import pprint

from selenium import webdriver

from action import constants
from action.config import parse_config
from action.login import login_sequence
from screen.resource import ResourceScreen
from screen.installations import InstallationScreen
from screen.galaxie import GalaxyScreen


def launch_bot():
    username, password, url = parse_config()

    driver = webdriver.Firefox()
    try:
        driver.get(url)
        print("Loaded page.")

        login_sequence(driver, username, password)
        with ResourceScreen(driver) as resource_tab:
            pprint(resource_tab.extract_info())

        with InstallationScreen(driver) as installation_tab:
            pprint(installation_tab.extract_info())

        with  GalaxyScreen(driver) as galaxy_tab:
            galaxy_tab.next_system()
            galaxy_tab.next_galaxy()
            galaxy_tab.prev_system()
            galaxy_tab.prev_galaxy()
            galaxy_tab.change_system(2,200)

        input("Waiting...")
    finally:
        driver.quit()


if __name__ == "__main__":
    launch_bot()
