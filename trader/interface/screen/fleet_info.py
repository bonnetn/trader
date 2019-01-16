# coding=utf-8
"""
Fleet information screen package.
"""
from collections import namedtuple
from typing import List, Dict

from selenium.common.exceptions import NoSuchElementException

from trader.interface.constants import TIMEOUT
from trader.interface.screen.generic_screen import GenericScreen, Planet
from trader.util.log import LOG

FLEET_INFO_BUTTON_XPATH = '/html/body/div[2]/div[2]/div/div[2]/div/ul/li[8]/span/a/div'
FRIENDLY_ROW_XPATH = '//*[contains(@class,"fleetDetails")]'
COME_BACK_XPATH = './/span/a[contains(@class,"icon_link")]'

HOSTILE_ROW_XPATH = '//*[contains(@class,"eventFleet")]'
HOSTILE_COUNTDOWN_XPATH = './/*[contains(@class,"countDown")]'
HOSTILE_DEST_FLEET_XPATH = './/*[contains(@class,"destFleet")]'
HOSTILE_DEST_COORDS_XPATH = './/*[contains(@class,"destCoords")]/a'

FleetMovement = namedtuple('FleetMovement', ['time1', 'time2', 'mission', 'src', 'dst'])


class FleetInfoScreen(GenericScreen):
    """
    Interface for the screen where you can see all of your ongoing missions.
    """

    def order_come_back(self, src):
        """
        Cancel a ghost mission.
        :param src: source planet
        """
        rows = self.driver.find_elements_by_xpath(FRIENDLY_ROW_XPATH)
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
                        LOG.exception("Could not unghost fleet.")
        raise Exception("Could not ghost specified fleet.")

    def extract_info(self) -> Dict[str, List[FleetMovement]]:
        """
        Get all the ongoing missions.
        :return: The missions.
        """
        friendly_rows = self.driver.find_elements_by_xpath(FRIENDLY_ROW_XPATH)
        friendly_rows = map(lambda x: self._extract_friendly_row_info(x), friendly_rows)
        friendly_rows = list(friendly_rows)

        hostile_rows = self.driver.find_elements_by_xpath(HOSTILE_ROW_XPATH)
        hostile_rows = filter(_is_hostile, hostile_rows)
        hostile_rows = map(_extract_hostile_row_info, hostile_rows)
        hostile_rows = list(hostile_rows)

        return {
            "friendly": friendly_rows,
            "hostile": hostile_rows
        }

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def move(self):
        """
        Move to the resource screen by clicking on the menu on the right.
        """
        self.driver.implicitly_wait(TIMEOUT)
        self.driver.find_element_by_xpath(FLEET_INFO_BUTTON_XPATH).click()
        self.driver.find_element_by_id("messages_collapsed").click()

    def _extract_friendly_row_info(self, row) -> FleetMovement:
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
            Planet(destination_coords, destination_planet),
        )


def _extract_hostile_row_info(r) -> FleetMovement:
    tr = r.find_element_by_xpath(HOSTILE_COUNTDOWN_XPATH)
    countdown = tr.text
    dest_name = r.find_element_by_xpath(HOSTILE_DEST_FLEET_XPATH).text
    dest_coords = r.find_element_by_xpath(HOSTILE_DEST_COORDS_XPATH).text
    return FleetMovement(
        time1=countdown,
        time2=None,
        mission='Attaquer',
        src=None,
        dst=Planet(name=dest_name, coord=dest_coords)
    )


def _is_hostile(r) -> bool:
    tr = r.find_element_by_xpath(HOSTILE_COUNTDOWN_XPATH)
    return "hostile" in tr.get_attribute('class')
