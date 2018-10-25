"""
Common constants
"""

TIMEOUT = 30

METAL = "metal"
CRYSTAL = "crystal"
DEUTERIUM = "deuterium"
ENERGY = "energy"
ALL_RESOURCES = [METAL, CRYSTAL, DEUTERIUM, ENERGY]

PLAY_BUTTON_XPATH = '//*[@id="accountlist"]/div/div[1]/div[2]/div/div/div[11]/button'

RESOURCE_BUTTON_XPATH = '//*[@id="menuTable"]/li[2]/a'

INSTALLATION_BUTTON_XPATH = '//*[@id="menuTable"]/li[3]/a'

GALAXY_BUTTON_XPATH = '//*[@id="menuTable"]/li[9]/a'

# Fields that you can find as keys in a result
RESULT_RESOURCE = "resources"
RESULT_LEVEL = "level"
