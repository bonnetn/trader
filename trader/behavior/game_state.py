from __future__ import annotations

from trader.behavior.context import Context


class GameState:
    """
    A state is part of the finite state machine of the bot. The bot moves from state to state while working.
    """
    def run(self, ctx: Context) -> GameState:
        raise NotImplementedError()
