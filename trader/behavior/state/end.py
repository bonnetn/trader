from trader.behavior.context import Context
from trader.behavior.game_state import GameState
from trader.log import LOG


class EndState(GameState):
    def run(self, ctx: Context) -> GameState:
        LOG.debug("End state reached.")
        return self


endState = EndState()
