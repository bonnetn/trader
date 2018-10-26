from selenium.common.exceptions import NoSuchElementException

from action.constants import TIMEOUT, RESULT_RESOURCE, RESULT_LEVEL
from tab.all import extract_resources_in_header

CURRENT_BUILDING_XPATH = '/html/body/div[2]/div[2]/div/div[3]/div[2]/div[5]/div[2]/table/tbody/tr[1]/th'
LEVEL_CONSTRUCTION_XPATH = '//li[@id="button{}"]//span[@class="level"]'
BUILD_BUTTON = "/html/body/div[2]/div[2]/div/div[3]/div[2]/div[4]/div[2]/ul[1]/li[{}]/div/div/a[1]"


METAL_MINE = "metal_mine"
CRYSTAL_MINE = "crystal_mine"
DEUTERIUM_MINE = "deuterium_mine"
SOLAR = "solar"

RESOURCE_TAB_ID_BUILDING = {
    METAL_MINE: 1,
    CRYSTAL_MINE: 2,
    DEUTERIUM_MINE: 3,
    SOLAR: 4,
}


class ResourceTab:
    def __init__(self, driver):
        self.driver = driver

    def extract_info(self):

        levels = {}
        for name, idBuilding in RESOURCE_TAB_ID_BUILDING.items():
            self.driver.implicitly_wait(TIMEOUT)
            levels[name] = self.driver.find_element_by_xpath(get_construction_level_xpath(idBuilding)).text

        result = {
            RESULT_LEVEL: levels,
        }
        try:
            self.driver.implicitly_wait(1)
            result["building"] = self.driver.find_element_by_xpath(CURRENT_BUILDING_XPATH).text
        except NoSuchElementException:
            result["building"] = False

        result[RESULT_RESOURCE] = extract_resources_in_header(self.driver)

        return result

    def build(self, building):
        self.driver.find_element_by_xpath(get_build_button_xpath(building)).click()


def get_build_button_xpath(building):
    return BUILD_BUTTON.format(RESOURCE_TAB_ID_BUILDING[building])


def get_construction_level_xpath(building):
    return LEVEL_CONSTRUCTION_XPATH.format(building)
