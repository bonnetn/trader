from trader.interface.base_screen import Screen
from trader.interface.constants import GLOBAL_VIEW_BUTTON_XPATH, TIMEOUT
from trader.util.log import LOG

box = ""
PLANETS = '//*[@id="planetList"]'
SHIP_BUTTON_XPATH = '//*[@id="messages_collapsed"]'
ROW_XPATH = '//*[@id="eventContent"]/tbody/tr'
FIELDS = ["arrivalTime", "originFleet", "coordsOrigin",
          "detailsFleet", "destFleet", "destCoords"]


class GlobalViewScreen(Screen):
    """
    """

    @staticmethod
    def _extract_fleet_info(row):
        data = dict(map(lambda x: (x, row.find_element_by_class_name(x).text), FIELDS))
        c = row.find_element_by_class_name("countDown").get_attribute("class")
        data["hostile"] = "hostile" in c
        return data

    def extract_info(self) -> dict:
        self.driver.implicitly_wait(TIMEOUT)
        self.driver.find_element_by_xpath(SHIP_BUTTON_XPATH).click()
        LOG.info("Clicked on the ship messsages.")

        rows = self.driver.find_elements_by_xpath(ROW_XPATH)
        fleet_info = list(map(GlobalViewScreen._extract_fleet_info, rows))
        LOG.info("Extracted fleet information.")

        planets = self.driver.find_element_by_xpath(PLANETS)
        planets = planets.find_elements_by_class_name("planet-koords ")
        planets = map(lambda x: x.text, planets)
        planets = list(planets)

        return {
            "fleet_info": fleet_info,
            "planets": planets
        }

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def move(self):
        """
        Move to the resource screen by clicking on the menu on the right.
        """
        self.driver.implicitly_wait(TIMEOUT)
        self.driver.find_element_by_xpath(GLOBAL_VIEW_BUTTON_XPATH).click()
