from trader.behavior.context import Context
from trader.behavior.game_state import GameState
from trader.util.log import LOG


class EndState(GameState):
    """
    EndState is a special state that represents the end of the bot.
    """
    def run(self, ctx: Context) -> GameState:
        LOG.debug("End state reached.")
        return self


endState = EndState()
