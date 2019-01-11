from trader.interface.constants import TIMEOUT
from trader.interface.screen.generic_screen import GenericScreen
from trader.util.log import LOG

PLAY_BUTTON_XPATH = '//*[@id="accountlist"]/div/div[1]/div[2]/div/div/div[11]/button'


class LoginScreen(GenericScreen):
    def __init__(self, driver, url):
        super().__init__(driver)
        self.driver = driver
        self.url = url

    def extract_info(self) -> dict:
        return {}

    def move(self) -> None:
        self.driver.get(self.url)

    def login_sequence(self, username: str, password: str):
        """
        Execute the login sequence.
        """

        driver = self.driver
        driver.find_element_by_id("ui-id-1").click()
        driver.find_element_by_id("usernameLogin").send_keys(username)
        driver.find_element_by_id("passwordLogin").send_keys(password)

        driver.find_element_by_id("loginSubmit").click()
        LOG.debug("Clicked 'Log in'")

        driver.implicitly_wait(TIMEOUT)
        driver.find_element_by_xpath(PLAY_BUTTON_XPATH).click()
        LOG.debug("Chose the universe.")

        driver.switch_to.window(driver.window_handles[1])
        LOG.debug("Switched to new screen.")
