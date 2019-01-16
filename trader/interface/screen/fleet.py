"""
Fleet screen package.
"""
from selenium.common.exceptions import NoSuchElementException

from trader.interface.constants import TIMEOUT, FLEET_BUTTON_XPATH
from trader.interface.screen.generic_screen import GenericScreen
from trader.util.log import LOG

SENDALL_BUTTON_XPATH = '//*[@id="sendall"]'
CONTINUE_BUTTON_XPATH = '//*[@id="continue"]'

GALAXY_XPATH = '//*[@id="galaxy"]'
SYSTEM_XPATH = '//*[@id="system"]'
POSITION_XPATH = '//*[@id="position"]'
PLANET_BUTTON_XPATH = '//*[@id="pbutton"]'
MOON_BUTTON_XPATH = '//*[@id="mbutton"]'
TEN_PERC_XPATH = '/html/body/div[2]/div[2]/div/div[3]/form/div/div[4]/div[2]/div[1]/ul[1]/li[3]/div/a[1]'
ALL_RES_XPATH = '//*[@id="allresources"]'
TRANSPORT_XPATH = '//*[@id="missionButton4"]'
SEND_SHIPS_XPATH = '//*[@id="start"]'


class FleetScreen(GenericScreen):
    """
    Screen that represents the screen where you can see your fleet.
    """

    def extract_info(self) -> dict:
        """
        Extract fleet information.
        :return:
        """
        return {}

    def ghost_all(self, pos) -> None:
        """
        Ghost all fleet from the current planet to the specified position.
        :param pos: Ghost fleet to this position.
        """
        self.driver.implicitly_wait(TIMEOUT)
        try:
            self.driver.implicitly_wait(TIMEOUT)
            self.driver.find_element_by_xpath(SENDALL_BUTTON_XPATH).click()
        except NoSuchElementException:
            LOG.info("No ship to ghost.")
            return
        self.driver.find_element_by_xpath(CONTINUE_BUTTON_XPATH).click()

        self.driver.implicitly_wait(TIMEOUT)
        self.driver.find_element_by_xpath(GALAXY_XPATH).clear()
        self.driver.find_element_by_xpath(GALAXY_XPATH).send_keys(str(pos[0]))
        self.driver.find_element_by_xpath(SYSTEM_XPATH).clear()
        self.driver.find_element_by_xpath(SYSTEM_XPATH).send_keys(str(pos[1]))
        self.driver.find_element_by_xpath(POSITION_XPATH).clear()
        self.driver.find_element_by_xpath(POSITION_XPATH).send_keys(str(pos[2]))
        self.driver.find_element_by_xpath(TEN_PERC_XPATH).click()
        if pos[3] == "PLANET":
            self.driver.find_element_by_xpath(PLANET_BUTTON_XPATH).click()
        else:
            self.driver.find_element_by_xpath(MOON_BUTTON_XPATH).click()

        self.driver.find_element_by_xpath(CONTINUE_BUTTON_XPATH).click()

        self.driver.implicitly_wait(TIMEOUT)
        self.driver.find_element_by_xpath(TRANSPORT_XPATH).click()
        self.driver.find_element_by_xpath(ALL_RES_XPATH).click()
        self.driver.find_element_by_xpath(SEND_SHIPS_XPATH).click()
        LOG.info("Ghosted")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def move(self):
        """
        Move to the resource screen by clicking on the menu on the right.
        """
        self.driver.implicitly_wait(TIMEOUT)
        self.driver.find_element_by_xpath(FLEET_BUTTON_XPATH).click()
