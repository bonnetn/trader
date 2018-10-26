from pprint import pprint

from selenium import webdriver

from action import constants
from action.config import parse_config
from action.constants import RESOURCE_BUTTON_XPATH
from action.constants import MAIN_BUTTON_XPATH
from action.login import login_sequence
from tab.resource import ResourceTab
from tab.infos import PointTab


def launch_bot():
    username, password, url = parse_config()

    driver = webdriver.Firefox()
    try:
        driver.implicitly_wait(constants.TIMEOUT)
        driver.get(url)
        print("Loaded page.")

        login_sequence(driver, username, password)
        	

        switch_to_main_tab(driver)

        points = PointTab(driver)
        pprint(points.extract_info())


        switch_to_resource_tab(driver)
        resource_tab = ResourceTab(driver)

       

        pprint(resource_tab.extract_info())
        # resource_tab.build(SOLAR)

        input("Waiting...")
    finally:
        driver.quit()


def switch_to_resource_tab(driver):
    driver.find_element_by_xpath(RESOURCE_BUTTON_XPATH).click()

def switch_to_main_tab(driver):
    driver.find_element_by_xpath(MAIN_BUTTON_XPATH).click()


if __name__ == "__main__":
    launch_bot()
