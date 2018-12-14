from trader.interface.base_screen import Screen
from trader.interface.constants import GLOBAL_VIEW_BUTTON_XPATH, TIMEOUT



class GlobalViewScreen(Screen):
    """
    """

    def extract_info(self) -> dict:
        return {}

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def move(self):
        """
        Move to the resource screen by clicking on the menu on the right.
        """
        self.driver.implicitly_wait(TIMEOUT)
        self.driver.find_element_by_xpath(GLOBAL_VIEW_BUTTON_XPATH).click()
