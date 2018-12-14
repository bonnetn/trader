import time

from selenium import webdriver

from trader.behavior.context import Context
from trader.behavior.state.attack_detection import attackDetection
from trader.behavior.state.login import loginState
from trader.util.log import LOG


def run_bot() -> None:
    LOG.info("Launching bot.")
    ctx = Context()

    while True:
        driver = webdriver.Firefox()
        ctx.driver = driver
        try:
            loginState.run(ctx)
            attackDetection.run(ctx)
        except KeyboardInterrupt:
            LOG.debug("Stop signal received.")
            return
        finally:
            LOG.info("Bot ended.")
            driver.quit()

        LOG.info("Sleeping for {}".format(ctx.next_sleep))
        time.sleep(ctx.next_sleep.total_seconds())
