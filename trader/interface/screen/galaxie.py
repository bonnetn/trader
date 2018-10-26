from trader.interface.action.constants import TIMEOUT, GALAXY_BUTTON_XPATH
from trader.interface.base_screen import Screen

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
        self.driver.implicitly_wait(TIMEOUT)
        self.driver.find_element_by_xpath(XPATH_NEXT_SYSTEM).click()

    def prev_system(self):
        self.driver.implicitly_wait(TIMEOUT)
        self.driver.find_element_by_xpath(XPATH_PREV_SYSTEM).click()

    def next_galaxy(self):
        self.driver.implicitly_wait(TIMEOUT)
        self.driver.find_element_by_xpath(XPATH_NEXT_GALAXY).click()

    def prev_galaxy(self):
        self.driver.implicitly_wait(TIMEOUT)
        self.driver.find_element_by_xpath(XPATH_PREV_GALAXY).click()
       

    def change_system(self, galaxie, system):
        
        self.driver.find_element_by_id("galaxy_input").send_keys(galaxie)
        self.driver.find_element_by_id("system_input").send_keys(system)

        self.driver.find_element_by_xpath(XPATH_CHANGE_BUTTON).click()

        self.driver.implicitly_wait(TIMEOUT)

    def planete_system(self):
        self.driver.implicitly_wait(TIMEOUT)
        content = self.driver.find_elements_by_css_selector('tr.row')
        planet = { }
        planet["habitee"]={}
        planet["inhabitee"]=[]
        for elt in content :
            classe = elt.get_attribute("class")
            if(classe == """row empty_filter
                                                """):
                planet["inhabitee"].append(elt.find_element_by_class_name("position").text)
            else:
                planet["habitee"][elt.find_element_by_class_name("position").text]=(elt.find_element_by_class_name("planetname").text,elt.find_element_by_class_name("playername").text)

        
        return planet

    def move(self):
        """
        Move to the resource screen by clicking on the menu on the right.
        """
        self.driver.find_element_by_xpath(GALAXY_BUTTON_XPATH).click()

