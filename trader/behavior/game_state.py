from trader.behavior.context import Context


class GameState:  #  Forward declaration, needed for type hinting.
    pass


class GameState:
    def run(self, ctx: Context) -> GameState:
        raise NotImplementedError()
