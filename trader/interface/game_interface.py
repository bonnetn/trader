"""
Game interface package.
"""
from selenium.webdriver.remote.webdriver import WebDriver

from trader.interface.screen.fleet import FleetScreen
from trader.interface.screen.fleet_info import FleetInfoScreen
from trader.interface.screen.generic_screen import Planet
from trader.interface.screen.login import LoginScreen
from trader.util.log import LOG


class GameInterface:
    """
    Facade interface between the bot and the game.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def log_in(self, config: tuple) -> None:
        """
        Log in the game.
        :param config: configuration class
        """
        username, password, url = config

        with LoginScreen(self.driver, url) as screen:
            screen.login_sequence(username, password)

        LOG.info("Logged in.")

    def get_planets_and_missions(self):
        """
        Retrieve planets and missions related information.
        :return:
        """
        with FleetInfoScreen(self.driver) as screen:
            my_planets = screen.extract_planets()
            missions = screen.extract_info()

        return my_planets, missions

    def ghost(self, src: Planet, dst_coords: list) -> None:
        """
        Ghost the fleet from a planet to another.
        :param src: source planet
        :param dst_coords: destination planet
        """
        with FleetScreen(self.driver) as screen:
            screen.select_planet(src)
            screen.ghost_all(dst_coords)

    def retrieve_fleet(self, src) -> None:
        """
        Retrieve the fleet ghosted from a planet.
        :param src: planet ghosted
        """
        with FleetInfoScreen(self.driver) as screen:
            screen.select_planet(src)
        with FleetInfoScreen(self.driver) as screen:
            screen.order_come_back(src)
