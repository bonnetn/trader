from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from trader.behavior.context import Context
from trader.behavior.state.end import endState
from trader.behavior.state.login import loginState
from trader.interface.constants import TIMEOUT
from trader.util.log import LOG


def launch_bot() -> None:
    LOG.info("Launching bot.")
    driver = webdriver.Firefox()
    try:
        ctx = Context(driver)
        while run_state_machine(driver, ctx):  #  Relaunch the state machine if it returns True.
            pass
    except KeyboardInterrupt:
        LOG.debug("Stop signal received.")
    finally:
        LOG.info("Bot ended.")
        driver.quit()


def run_state_machine(driver, ctx: Context) -> bool:
    state = loginState
    try:
        while state != endState:
            state = state.run(ctx)
        return False

    except WebDriverException:
        if is_on_login_screen(driver):
            LOG.info('Logged out. Restarting bot.')
            return True  # Relaunch the bot
        raise  #  If we are not on login screen but we still have an error, re-raise the exception.


def is_on_login_screen(driver) -> bool:
    driver.implicitly_wait(TIMEOUT)
    return bool(driver.find_elements_by_id("loginForm"))
