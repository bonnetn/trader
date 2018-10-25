from action.config import parse_config
from action.login import login_sequence
from behavior.context import Context
from behavior.game_state import GameState
from behavior.state.end import endState
from log import LOG


class LoginState(GameState):
    def run(self, ctx: Context) -> GameState:
        d = ctx.driver

        username, password, url = parse_config()

        d.get(url)
        login_sequence(d, username, password)
        LOG.info("Logged in.")

        return endState


loginState = LoginState()
