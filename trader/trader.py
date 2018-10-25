from selenium import webdriver

from trader.behavior.context import Context
from trader.behavior.state.end import endState
from trader.behavior.state.login import loginState
from trader.util.log import LOG


def launch_bot():
    LOG.info("Launching bot.")
    driver = webdriver.Firefox()
    try:
        ctx = Context(driver)
        state = loginState
        while state != endState:
            state = state.run(ctx)
    finally:
        LOG.info("Bot ended.")
        driver.quit()
