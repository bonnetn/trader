from trader.interface.action.constants import TIMEOUT, GALAXY_BUTTON_XPATH
from trader.interface.screen import Screen

XPATH_CHANGE_BUTTON = '//*[@id="galaxyHeader"]/form/div'
XPATH_NEXT_SYSTEM = '//*[@id="galaxyHeader"]/form/span[6]'
XPATH_PREV_SYSTEM = '//*[@id="galaxyHeader"]/form/span[5]'
XPATH_NEXT_GALAXY = '//*[@id="galaxyHeader"]/form/span[3]'
XPATH_PREV_GALAXY = '//*[@id="galaxyHeader"]/form/span[2]'


class GalaxyScreen(Screen):
    """
    InstallationTab represents the page where you can see all your buildings that produce/store resources.
    """

    def extract_info(self) -> dict:
        return {}

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def next_system(self):
        self.driver.find_element_by_xpath(XPATH_NEXT_SYSTEM).click()
        self.driver.implicitly_wait(TIMEOUT)

    def prev_system(self):
        self.driver.find_element_by_xpath(XPATH_PREV_SYSTEM).click()
        self.driver.implicitly_wait(TIMEOUT)

    def next_galaxy(self):
        self.driver.find_element_by_xpath(XPATH_NEXT_GALAXY).click()
        self.driver.implicitly_wait(TIMEOUT)

    def prev_galaxy(self):
        self.driver.find_element_by_xpath(XPATH_PREV_GALAXY).click()
        self.driver.implicitly_wait(TIMEOUT)

    def change_system(self, galaxie, system):
        """
        Execute the login sequence.
        """

        self.driver.find_element_by_id("galaxy_input").send_keys(galaxie)
        self.driver.find_element_by_id("system_input").send_keys(system)

        self.driver.find_element_by_xpath(XPATH_CHANGE_BUTTON).click()

        self.driver.implicitly_wait(TIMEOUT)

    def move(self):
        """
        Move to the resource screen by clicking on the menu on the right.
        """
        self.driver.find_element_by_xpath(GALAXY_BUTTON_XPATH).click()
