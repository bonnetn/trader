from selenium.common.exceptions import NoSuchElementException

from action.constants import TIMEOUT, RESULT_RESOURCE, RESULT_LEVEL, GALAXY_BUTTON_XPATH
from screen.screen import Screen

XPATH_CHANGE_BUTTON = '//*[@id="galaxyHeader"]/form/div'

class GalaxyScreen(Screen):
    """
    InstallationTab represents the page where you can see all your buildings that produce/store resources.
    """

    def __init__(self, driver):
        self.driver = driver

    def change_system(self,galaxie,system):
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
        
