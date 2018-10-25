from selenium import webdriver

from behavior.context import Context
from behavior.state.end import endState
from behavior.state.login import loginState
from log import LOG


def launch_bot():
    driver = webdriver.Firefox()
    try:
        ctx = Context(driver)
        state = loginState
        while state != endState:
            state = state.run(ctx)
    finally:
        driver.quit()


if __name__ == "__main__":
    LOG.info("Launching bot...")
    launch_bot()
    LOG.info("Bot ended.")
