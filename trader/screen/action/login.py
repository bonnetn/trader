from trader.screen.action.constants import PLAY_BUTTON_XPATH, TIMEOUT
from trader.log import LOG


def login_sequence(driver, username, password):
    """
    Execute the login sequence.
    """
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
