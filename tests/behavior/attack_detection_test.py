from datetime import datetime
from unittest.mock import Mock, call

import pytest

from trader.behavior.attack_detection import ghost_fleet_if_necessary, TIME_OFFSET, RETRIES_COUNT
from trader.interface.game_interface import GameInterface
from trader.interface.screen.fleet_info import FleetMovement
from trader.interface.screen.generic_screen import Planet


def test_ghost_cant_retrieve(planet1, planet2, ghost_mission, attack1):
    game = Mock(spec=GameInterface)
    ticks = set()

    my_planets = [planet1, planet2]
    missions = {
        "hostile": [attack1],
        "friendly": [ghost_mission],
    }

    game.get_planets_and_missions = Mock(return_value=(my_planets, missions))
    # noinspection PyTypeChecker
    ghost_fleet_if_necessary(game, ticks)
    game.retrieve_fleet.assert_not_called()


def test_ghost_retrieve(planet1, planet2, ghost_mission):
    game = Mock(spec=GameInterface)
    ticks = set()

    my_planets = [planet1, planet2]
    missions = {
        "hostile": [],
        "friendly": [ghost_mission],
    }

    game.get_planets_and_missions = Mock(return_value=(my_planets, missions))
    # noinspection PyTypeChecker
    ghost_fleet_if_necessary(game, ticks)
    game.retrieve_fleet.assert_called_once_with("[1:1:1]")


def test_ghost_cant_ghost(planet1, planet2, attack1):
    game = Mock(spec=GameInterface)
    ticks = set()

    my_planets = [planet1, planet2]
    missions = {
        "hostile": [attack1],
        "friendly": [],
    }

    game.get_planets_and_missions = Mock(return_value=(my_planets, missions))
    game.ghost = Mock(side_effect=Exception("Failed to ghost"))
    # noinspection PyTypeChecker
    ghost_fleet_if_necessary(game, ticks)
    assert game.ghost.call_count == RETRIES_COUNT


# noinspection PyTypeChecker
def test_ghost_planets_are_safe(planet1, planet2):
    game = Mock(spec=GameInterface)
    ticks = set()

    my_planets = [planet1, planet2]
    missions = {
        "hostile": [],
        "friendly": [],
    }

    game.get_planets_and_missions = Mock(return_value=(my_planets, missions))
    ghost_fleet_if_necessary(game, ticks)
    game.ghost.assert_not_called()


# noinspection PyTypeChecker
def test_ghost_two_planet_attacked(planet1, planet2, attack1, attack2):
    game = Mock(spec=GameInterface)
    ticks = set()

    my_planets = [planet1, planet2]
    missions = {
        "hostile": [attack1, attack2],
        "friendly": [],
    }

    game.get_planets_and_missions = Mock(return_value=(my_planets, missions))
    ghost_fleet_if_necessary(game, ticks)
    assert game.ghost.call_count == 2
    game.ghost.assert_has_calls([
        call(planet1, ['2', '2', '2', 'PLANET']),
        call(planet2, ['1', '1', '1', 'PLANET']),
    ], any_order=True)


# noinspection PyTypeChecker
def test_ghost_one_planet_attacked(planet1, planet2, attack1):
    game = Mock(spec=GameInterface)
    ticks = set()

    my_planets = [planet1, planet2]
    missions = {
        "hostile": [attack1],
        "friendly": [],
    }

    game.get_planets_and_missions = Mock(return_value=(my_planets, missions))
    ghost_fleet_if_necessary(game, ticks)
    game.ghost.assert_called_once_with(planet1, ['2', '2', '2', 'PLANET'])


# noinspection PyTypeChecker
def test_ghost_wait_before_attack(planet1, planet2):
    game = Mock(spec=GameInterface)
    ticks = set()

    my_planets = [planet1, planet2]
    missions = {
        "hostile": [FleetMovement(
            time1="30h",
            time2=None,
            mission="Attaquer",
            src="[666:666:666]",
            dst="[1:1:1]"
        )],
        "friendly": [],
    }

    game.get_planets_and_missions = Mock(return_value=(my_planets, missions))
    ghost_fleet_if_necessary(game, ticks)

    game.ghost.assert_not_called()

    assert len(ticks) == 1
    time = next(iter(ticks))
    assert time > datetime.now(), "Next trigger must be in the future"
    assert time - datetime.now() >= TIME_OFFSET


@pytest.fixture
def attack1():
    return FleetMovement(
        time1="3s",
        time2=None,
        mission="Attaquer",
        src="[666:666:666]",
        dst="[1:1:1]"
    )


@pytest.fixture
def attack2():
    return FleetMovement(
        time1="3s",
        time2=None,
        mission="Attaquer",
        src="[666:666:666]",
        dst="[2:2:2]"
    )


@pytest.fixture
def ghost_mission():
    return FleetMovement(
        time1="3s",
        time2="6s",
        mission="Stationner",
        src="[1:1:1]",
        dst="[2:2:2]"
    )


@pytest.fixture
def planet1():
    return Planet(coord="[1:1:1]", name="Planet1")


@pytest.fixture
def planet2():
    return Planet(coord="[2:2:2]", name="Planet2")
