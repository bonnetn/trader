"""
All is a module that contains misc. function that can be called from everywhere.
"""
from action.constants import ALL_RESOURCES, METAL, CRYSTAL, DEUTERIUM, ENERGY, TIMEOUT

XPATH_COUNTER = {
    METAL: '//*[@id="resources_metal"]',
    CRYSTAL: '//*[@id="resources_crystal"]',
    DEUTERIUM: '//*[@id="resources_deuterium"]',
    ENERGY: '//*[@id="resources_energy"]',
}


def extract_resources_in_header(driver):
    """
    Extraxt the resource count from the top band.
    :param driver:
    :return: a dictionnary, which binds a resource to an amount
    """
    result = {}
    for res in ALL_RESOURCES:
        driver.implicitly_wait(TIMEOUT)
        result[res] = driver.find_element_by_xpath(XPATH_COUNTER[res]).text

    return result
