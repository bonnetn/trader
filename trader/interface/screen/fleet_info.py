import time

from selenium.common.exceptions import NoSuchElementException

from trader.interface.constants import TIMEOUT
from trader.interface.screen.generic_screen import GenericScreen, Planet

FLEET_INFO_BUTTON_XPATH = '/html/body/div[2]/div[2]/div/div[2]/div/ul/li[8]/span/a/div'
ROW_XPATH = '//*[contains(@class,"fleetDetails")]'
COME_BACK_XPATH = './/span/a[contains(@class,"icon_link")]'

from collections import namedtuple

FleetMovement = namedtuple('FleetMovement', ['time1', 'time2', 'mission', 'src', 'dst'])


class FleetInfoScreen(GenericScreen):
    """
    """

    def order_come_back(self, src):
        rows = self.driver.find_elements_by_xpath(ROW_XPATH)
        for row in rows:
            if row.find_element_by_class_name("mission").text == "Stationner":

                origin_data = row.find_element_by_class_name("originData")
                origin_coords = origin_data.find_element_by_xpath('.//*[contains(@class,"originCoords")]/a').text
                origin_planet = origin_data.find_element_by_class_name("originPlanet").text

                if origin_planet == src.name and origin_coords == src.coord:
                    try:
                        self.driver.implicitly_wait(0)
                        row.find_element_by_xpath(COME_BACK_XPATH).click()
                        return
                    except NoSuchElementException:
                        LOG.warning("Could not unghost fleet.")
        raise Exception("Could not ghost specified fleet.")


    def _extract_info_from_row(self, row):
        mission = row.find_element_by_class_name("mission")
        mission = mission.text

        origin_data = row.find_element_by_class_name("originData")
        origin_coords = origin_data.find_element_by_xpath('.//*[contains(@class,"originCoords")]/a').text
        origin_planet = origin_data.find_element_by_class_name("originPlanet").text

        destination_data = row.find_element_by_class_name("destinationData")
        destination_coords = destination_data.find_element_by_xpath('.//*[contains(@class,"destinationCoords")]/a').text
        destination_planet = destination_data.find_element_by_class_name("destinationPlanet").text

        try:
            self.driver.implicitly_wait(0)
            next_timer = row.find_element_by_class_name("nextTimer")
            next_time = next_timer.text
        except NoSuchElementException:
            next_time = None

        timer = row.find_element_by_class_name("timer")
        timer = timer.text

        return FleetMovement(
            timer, next_time,
            mission,
            Planet(origin_coords, origin_planet),
            Planet(destination_coords, destination_planet),  # inverted for testing
        )

    def extract_info(self) -> dict:
        rows = self.driver.find_elements_by_xpath(ROW_XPATH)
        rows = map(lambda x: self._extract_info_from_row(x), rows)
        rows = list(rows)
        return rows

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def move(self):
        """
        Move to the resource screen by clicking on the menu on the right.
        """
        self.driver.implicitly_wait(TIMEOUT)
        self.driver.find_element_by_xpath(FLEET_INFO_BUTTON_XPATH).click()
