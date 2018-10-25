from selenium.common.exceptions import NoSuchElementException

from trader.interface.action.constants import TIMEOUT, RESULT_LEVEL, INSTALLATION_BUTTON_XPATH
from trader.interface.screen.screen import Screen

CURRENT_BUILDING_XPATH = '/html/body/div[2]/div[2]/div/div[3]/div[2]/div[5]/div[2]/table/tbody/tr[1]/th'
LEVEL_CONSTRUCTION_XPATH = '//li[@id="button{}"]//span[@class="level"]'
BUILD_BUTTON = "/html/body/div[2]/div[2]/div/div[3]/div[2]/div[4]/div[2]/ul[1]/li[{}]/div/div/a[1]"

USINE_ROBOT = "usine_de_robot"
CHANTIER_SPATIAL = "chantier_spatial"
LABORATOIRE = "laboratoire"
DEPOT_RAVITAILLEMENT = "depot_de_ravitaillement"
SILO_MISSILE = "silo_de_missile"
USINE_NANITE = "usine_de_nanite"
TERRAFORMEUR = "terraformeur"
DOCK_SPATIAL = "dock_spatial"

INSTALLATION_TAB_ID_BUILDING = {
    USINE_ROBOT: 0,
    CHANTIER_SPATIAL: 1,
    LABORATOIRE: 2,
    DEPOT_RAVITAILLEMENT: 3,
    SILO_MISSILE: 4,
    USINE_NANITE: 5,
    TERRAFORMEUR: 6,
    DOCK_SPATIAL: 7,
}


class InstallationScreen(Screen):
    """
    InstallationTab represents the page where you can see all your buildings that produce/store resources.
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
        for name, idBuilding in INSTALLATION_TAB_ID_BUILDING.items():
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

        # result[RESULT_RESOURCE] = extract_resources_in_header(self.driver)

        return result

    def move(self):
        """
        Move to the resource screen by clicking on the menu on the right.
        """
        self.driver.find_element_by_xpath(INSTALLATION_BUTTON_XPATH).click()

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
    return BUILD_BUTTON.format(INSTALLATION_TAB_ID_BUILDING[building])


def get_construction_level_xpath(building):
    """
    Return the XPath of the span tags that contain the construction level of the building.
    :param building:
    """
    return LEVEL_CONSTRUCTION_XPATH.format(building)
