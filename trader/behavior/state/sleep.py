import time

from trader.behavior.context import Context
from trader.behavior.game_state import GameState
from trader.util.log import LOG

SECOND = 1
MINUTE = 60
HOUR = 60 * MINUTE


class Sleep(GameState):
    def __init__(self, next_state, duration):
        self.next_state = next_state
        self.duration = duration

    def run(self, ctx: Context) -> GameState:
        LOG.info("Sleeping for {} seconds.".format(self.duration))
        time.sleep(self.duration)
        LOG.debug("Woke up!")
        return self.next_state
