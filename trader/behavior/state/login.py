from trader.behavior.context import Context
from trader.behavior.game_state import GameState
from trader.interface.screen.login import LoginScreen
from trader.util.config import parse_config
from trader.util.log import LOG


class LoginState(GameState):
    def run(self, ctx: Context) -> GameState:
        username, password, url = parse_config()

        with LoginScreen(ctx.driver, url) as screen:
            screen.login_sequence(username, password)
        LOG.info("Logged in.")

        return None


loginState = LoginState()
