from action.constants import ALL_RESOURCES, METAL, CRYSTAL, DEUTERIUM, ENERGY, TIMEOUT

XPATH_COUNTER = {
    METAL: '//*[@id="resources_metal"]',
    CRYSTAL: '//*[@id="resources_crystal"]',
    DEUTERIUM: '//*[@id="resources_deuterium"]',
    ENERGY: '//*[@id="resources_energy"]',
}


def extract_resources_in_header(driver):
    result = {}
    for res in ALL_RESOURCES:
        driver.implicitly_wait(TIMEOUT)
        print(res)
        print(XPATH_COUNTER[res])
        result[res] = driver.find_element_by_xpath(XPATH_COUNTER[res]).text

    return result
