from selenium.common.exceptions import NoSuchElementException

from action.constants import TIMEOUT, RESULT_INFO
from tab.all import extract_resources_in_header
from time import sleep



SPACE1 = "espace_occupee"
SPACE2 = "espace_maximum"
POSITION = "coordonees"
POINT = "points"
HONOR = "points_honorifiques"

INFO_TAB_XPATH = {
    SPACE1: '//*[@id="diameterContentField"]/span[1]',
    SPACE2: '//*[@id="diameterContentField"]/span[2]',
    POSITION: '//*[@id="positionContentField"]/a',
    POINT: '//*[@id="scoreContentField"]/a',
    HONOR: '//*[@id="honorContentField"]',
}


class PointTab:
    def __init__(self, driver):
        self.driver = driver

    def extract_info(self):
        sleep(2)
        levels = {}
        for name, info_xpath in INFO_TAB_XPATH.items():
            self.driver.implicitly_wait(TIMEOUT)
            levels[name] = self.driver.find_element_by_xpath(info_xpath).text
            print(levels[name])
        result = {
            RESULT_INFO: levels,
        }
        return result


