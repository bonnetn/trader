from selenium.common.exceptions import NoSuchElementException

from trader.interface.action.constants import TIMEOUT, RESULT_RESOURCE, RESULT_LEVEL, RESOURCE_BUTTON_XPATH
from trader.interface.screen.generic_screen import GenericScreen

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


class ResourceScreen(GenericScreen):
    """
    ResourceScreen represents the page where you can see all your buildings that produce/store resources.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def extract_info(self):
        """
        Extract the resources, levels of the buildings and the building currently being built.
        :return: a dictionnary
        """
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

        result[RESULT_RESOURCE] = self.extract_resources()

        return result

    def move(self):
        """
        Move to the resource screen by clicking on the menu on the right.
        """
        self.driver.find_element_by_xpath(RESOURCE_BUTTON_XPATH).click()

    def build(self, building):
        """
        Order the construction of a building.
        :param building: building to construct
        """
        self.driver.find_element_by_xpath(get_build_button_xpath(building)).click()


def get_build_button_xpath(building):
    """
    Get the XPath from the button to build a specific building.
    :param building: building to construct
    """
    return BUILD_BUTTON.format(RESOURCE_TAB_ID_BUILDING[building])


def get_construction_level_xpath(building):
    """
    Return the XPath of the span tags that contain the construction level of the building.
    :param building:
    """
    return LEVEL_CONSTRUCTION_XPATH.format(building)
