import datetime
import time
from typing import Set, Callable

from trader.behavior.attack_detection import ghost_fleet_if_necessary
from trader.interface.game_interface import GameInterface
from trader.util.log import LOG
from trader.util.time import remove_dates_in_past, get_closest_datetime


class Bot:
    def _trigger_bot(self, game: GameInterface, ticks: Set[datetime.datetime]) -> None:
        """
        Trigger main algorithm of the bot.
        :param game: Game interface
        :param ticks: Set of datetime of when to trigger the bot again.
        """
        game.log_in(self.config)
        ghost_fleet_if_necessary(game, ticks)  # Will ghost the fleet on threatened planets.

    def __init__(self, config: tuple, get_driver: Callable):
        self.config = config
        self.get_driver = get_driver

    def run(self) -> None:
        """
        Run the bot.
        """
        ticks: Set[datetime] = []  # When to trigger the bot

        while True:
            self._loop(ticks)

    def _loop(self, ticks: Set[datetime.datetime]) -> None:
        with self.get_driver() as driver:
            game = GameInterface(driver)
            self._trigger_bot(game, ticks)

        time_to_sleep = datetime.timedelta(minutes=20)
        if ticks:
            ticks = remove_dates_in_past(ticks)
            next_sleep = get_closest_datetime(ticks)
            time_to_sleep = min(time_to_sleep, next_sleep)

        LOG.info("Sleeping for {}".format(time_to_sleep))
        time.sleep(time_to_sleep.total_seconds())
