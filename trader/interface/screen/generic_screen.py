"""
All is a module that contains misc. function that can be called from everywhere.
"""
from trader.interface.constants import ALL_RESOURCES, METAL, CRYSTAL, DEUTERIUM, ENERGY, TIMEOUT
from trader.interface.base_screen import Screen

XPATH_COUNTER = {
    METAL: '//*[@id="resources_metal"]',
    CRYSTAL: '//*[@id="resources_crystal"]',
    DEUTERIUM: '//*[@id="resources_deuterium"]',
    ENERGY: '//*[@id="resources_energy"]',
}


class GenericScreen(Screen):
    def extract_info(self) -> dict:
        raise NotImplementedError()

    def move(self) -> None:
        raise NotImplementedError()

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
