import sqlite3

from trader.behavior.context import Context
from trader.behavior.game_state import GameState
from trader.behavior.state.sleep import Sleep, MINUTE
from trader.interface.screen.resource import RESOURCE_TAB_ID_BUILDING, ResourceScreen, CannotBuildException
from trader.util.log import LOG

TABLE_NAME = "construction_queue"
DB = sqlite3.connect("trader.db")

DB.execute('CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, building TEXT);'.format(TABLE_NAME))


class ConstructBuilding(GameState):
    @staticmethod
    def peek_queue() -> tuple:
        with DB:
            result = DB.execute("SELECT * FROM {} ORDER BY id LIMIT 1".format(TABLE_NAME)).fetchone()

        if result is None:
            return None, None
        return result

    @staticmethod
    def pop_queue(queue_id: int) -> None:
        with DB:
            DB.execute('DELETE FROM {} WHERE id={}'.format(TABLE_NAME, queue_id))

    def try_build_queue(self, screen: ResourceScreen) -> bool:
        """
        Try to build peek element in queue.
        :return: True if must retry to build.
        """
        queue_id, building = self.peek_queue()
        if queue_id is None:
            LOG.info("No construction left in the construction queue!")
            return False

        if building not in RESOURCE_TAB_ID_BUILDING:
            LOG.info("'{}' in construction queue not recognized, skipping.".format(building))
            self.pop_queue(queue_id)
            return True  #  Retry next construction in queue.

        LOG.debug("Next construction in queue: {}".format(building))

        try:
            screen.build(building)
        except CannotBuildException:
            LOG.info("Cannot build {}.".format(building))
            return False

        self.pop_queue(queue_id)
        LOG.info("Launched construction of {}".format(building))

        return True  #  Stay on this state until you cannot build anything.

    def run(self, ctx: Context) -> GameState:
        with ResourceScreen(ctx.driver) as screen:
            while self.try_build_queue(screen):
                pass

        return Sleep(self, 2 * MINUTE)


constructBuilding = ConstructBuilding()
