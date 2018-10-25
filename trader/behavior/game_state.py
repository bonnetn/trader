from __future__ import annotations

from trader.behavior.context import Context


class GameState:
    def run(self, ctx: Context) -> GameState:
        raise NotImplementedError()
