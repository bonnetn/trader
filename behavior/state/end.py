from behavior.context import Context
from behavior.game_state import GameState
from log import LOG


class EndState(GameState):
    def run(self, ctx: Context) -> GameState:
        LOG.debug("End state reached.")
        return self


endState = EndState()
