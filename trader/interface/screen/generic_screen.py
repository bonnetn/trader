"""
All is a module that contains misc. function that can be called from everywhere.
"""
from typing import List

from trader.interface.constants import ALL_RESOURCES, METAL, CRYSTAL, DEUTERIUM, ENERGY, TIMEOUT
from trader.interface.screen.base_screen import Screen
from trader.util.log import LOG

XPATH_COUNTER = {
    METAL: '//*[@id="resources_metal"]',
    CRYSTAL: '//*[@id="resources_crystal"]',
    DEUTERIUM: '//*[@id="resources_deuterium"]',
    ENERGY: '//*[@id="resources_energy"]',
}

PLANETS = '//*[@id="planetList"]'
SMALL_PLANET_XPATH = '//*[contains(@class,"smallplanet")]'

from collections import namedtuple

Planet = namedtuple('Planet', ['coord', 'name'])


class GenericScreen(Screen):
    def extract_info(self) -> dict:
        raise NotImplementedError()

    def move(self) -> None:
        raise NotImplementedError()

    def select_planet(self, target) -> None:
        planets = self.driver.find_elements_by_xpath(SMALL_PLANET_XPATH)
        for planet in planets:
            planet_coords = planet.find_element_by_class_name("planet-koords").text
            if planet_coords == target.coord:
                planet_name = planet.find_element_by_class_name("planet-name").text
                if planet_name == target.name:
                    LOG.debug("Selecting planet for {}".format(target))
                    planet.find_element_by_xpath('.//a[contains(@class, "planetlink")]').click()
                else:
                    LOG.debug("Selecting moon for {}".format(target))
                    planet.find_element_by_xpath('.//a[contains(@class, "moonlink")]').click()

                return

        raise Exception("Could not find planet {}".format(target))

    def extract_planets(self) -> List[Planet]:
        planets = self.driver.find_element_by_xpath(PLANETS)

        planet_names = planets.find_elements_by_class_name("planet-name")
        planet_coords = planets.find_elements_by_class_name("planet-koords")

        planets = zip(planet_coords, planet_names)
        planets = map(lambda x: Planet(x[0].text, x[1].text), planets)
        planets = list(planets)

        return planets

    def extract_resources(self):
        """
        Extract the resource count from the top band.
        :return: a dictionnary, which binds a resource to an amount
        """
        result = {}
        for res in ALL_RESOURCES:
            self.driver.implicitly_wait(TIMEOUT)
            result[res] = self.driver.find_element_by_xpath(XPATH_COUNTER[res]).text

        return result
