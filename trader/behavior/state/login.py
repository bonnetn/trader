from trader.behavior.state.end import endState
from trader.screen.action.config import parse_config
from trader.behavior.context import Context
from trader.behavior.game_state import GameState
from trader.log import LOG
from trader.screen.action.login import login_sequence


class LoginState(GameState):
    def run(self, ctx: Context) -> GameState:
        d = ctx.driver

        username, password, url = parse_config()

        d.get(url)
        login_sequence(d, username, password)
        LOG.info("Logged in.")

        return endState


loginState = LoginState()
