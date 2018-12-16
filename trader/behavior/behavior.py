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
        try:
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

            LOG.info("Sleeping for {}".format(ctx.sleep_for))
            time.sleep(ctx.sleep_for.total_seconds())
        except Exception:
            LOG.exception("Bot crashed, restarting...")
