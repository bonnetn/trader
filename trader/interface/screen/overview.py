from selenium.common.exceptions import NoSuchElementException

from trader.interface.action.constants import TIMEOUT, RESULT_INFO, RESULT_TASK
from time import sleep
from trader.interface.screen.generic_screen import GenericScreen


SPACE1 = "espace_occupee"
SPACE2 = "espace_maximum"
POSITION = "coordonees"
POINT = "points"
HONOR = "points_honorifiques"

INFO_TAB_XPATH = {
    SPACE1: '//*[@id="diameterContentField"]/span[1]',
    SPACE2: '//*[@id="diameterContentField"]/span[2]',
    POSITION: '//*[@id="positionContentField"]/a',
    POINT: '//*[@id="scoreContentField"]/a',
    HONOR: '//*[@id="honorContentField"]',
}



BUILDING_NAME = "building_name"
BUILDING_TIME = "building_time"


RESEARCH_NAME = "research_name"
RESEARCH_TIME = "research_time"


INSTALLATION_NAME = "installation_name"
INSTALLATION_TIME = "installation_time"

CURRENT_TASK_XPATH = {

BUILDING_NAME: '//*[@id="overviewBottom"]/div[1]/div[2]/table/tbody/tr[1]/th',
BUILDING_TIME: '//*[@id="overviewBottom"]/div[1]//*[@id="Countdown"]',

RESEARCH_NAME: '//*[@id="overviewBottom"]/div[2]/div[2]/table/tbody/tr[1]/th',
RESEARCH_TIME: '//*[@id="overviewBottom"]/div[2]//*[@id="Countdown"]',


INSTALLATION_NAME: '//*[@id="overviewBottom"]/div[3]/div[2]/table/tbody/tr[1]/th',
INSTALLATION_TIME: '//*[@id="overviewBottom"]/div[3]//*[@id="Countdown"]',



}


CURRENT_NONETASK_XPATH = {

BUILDING_NAME: '//*[@id="overviewBottom"]/div[1]/div[2]/table/tbody/tr/td/a[@class="tooltip js_hideTipOnMobile"]',
BUILDING_TIME: '//*[@id="overviewBottom"]/div[1]/div[2]/table/tbody/tr/td/a[@class="tooltip js_hideTipOnMobile"]',

RESEARCH_NAME: '//*[@id="overviewBottom"]/div[2]/div[2]/table/tbody/tr/td/a[@class="tooltip js_hideTipOnMobile"]',
RESEARCH_TIME: '//*[@id="overviewBottom"]/div[2]/div[2]/table/tbody/tr/td/a[@class="tooltip js_hideTipOnMobile"]',


INSTALLATION_NAME: '//*[@id="overviewBottom"]/div[3]/div[2]/table/tbody/tr/td/a[@class="tooltip js_hideTipOnMobile"]',
INSTALLATION_TIME: '//*[@id="overviewBottom"]/div[3]/div[2]/table/tbody/tr/td/a[@class="tooltip js_hideTipOnMobile"]',



}



class PointTab(GenericScreen):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def extract_info(self):

        
        sleep(5)
        result = {}
        levels = {}
        for name, info_xpath in INFO_TAB_XPATH.items():
            self.driver.implicitly_wait(TIMEOUT)
            levels[name] = self.driver.find_element_by_xpath(info_xpath).text
        result[RESULT_INFO] = levels

        task = {}
        for taskname, task_xpath in CURRENT_TASK_XPATH.items():
            self.driver.implicitly_wait(TIMEOUT)
           
            if(check(self,taskname)):
                task[taskname] = self.driver.find_element_by_xpath(task_xpath).text
            else:
                task[taskname] = "Aucun en cours"
                
        result[RESULT_TASK]= task
	
        return result

    def move(self):

        self.driver.find_element_by_xpath(MAIN_BUTTON_XPATH).click()

def check(self,taskname):
      try:
          self.driver.find_element_by_xpath(CURRENT_NONETASK_XPATH[taskname]).text
          return False;
      except:
          print("BITCHHHH")
          return True;
        


