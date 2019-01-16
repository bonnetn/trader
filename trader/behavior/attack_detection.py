"""
Definition of behavior of the bot when it will check for ongoing attacks.
"""
import random
from datetime import timedelta, datetime
from typing import Set, List

from trader.interface.game_interface import GameInterface
from trader.interface.screen.generic_screen import Planet
from trader.util.log import LOG
from trader.util.time import convert_to_timedelta

TIME_OFFSET = timedelta(minutes=5)
RETRIES_COUNT = 3


class CouldNotGhostException(Exception):
    """
    Failed attempt to ghost.
    """

    def __init__(self, planet: Planet):
        self.planet = planet


def ghost_fleet_if_necessary(game: GameInterface, ticks: Set[datetime]) -> None:
    """
    Ghost the fleet of planets that are threatened.
    :param game: Game interface
    :param ticks: List of datetimes when to wake the bot again.
    """
    # Get account information.
    my_planets, missions = game.get_planets_and_missions()

    # Extract relevant pieces of information.
    hostile_missions = missions["hostile"]
    friendly_missions = missions["friendly"]

    # Ghost fleet on every threatened planet.
    for planet in _get_planets_being_under_attacks(hostile_missions, my_planets):
        next_attack_time = _get_next_attack_time(hostile_missions, planet)

        if _should_ghost_fleet(next_attack_time):
            LOG.debug("Someone is attacking {}, ghosting everything...".format(planet.name))
            try:
                _try_to_ghost(planet, game, my_planets)
            except CouldNotGhostException:
                LOG.exception("Could not ghost planet {}, scheduling retry in 1 minute.".format(planet))
                ticks |= {datetime.now() + timedelta(minutes=1)}
            else:
                # Next wake up, 5 mins after attack to retrieve fleet.
                ticks |= {next_attack_time + TIME_OFFSET}
        else:
            log_msg = "Someone is attacking {} but we still have time ({}) to sleep..."
            LOG.debug(log_msg.format(planet.name, next_attack_time))

            # Next wake up, 5 mins before attack to ghost fleet.
            ticks |= {next_attack_time - TIME_OFFSET}

    # Order ghost fleet to come back if the planet is safe.
    for mission in _get_ghost_missions(friendly_missions):
        planet = next(filter(lambda x: x.coord == mission.src.coord, my_planets))
        attacks = _get_attacks_to_this_planet(hostile_missions, planet)
        if not attacks:
            game.retrieve_fleet(mission.src)
            LOG.info("{} is safe, retrieved ghost fleet.".format(mission.src))
        else:
            LOG.info("{} is still threatened.".format(mission.src))


def _should_ghost_fleet(attack_time: datetime) -> bool:
    time_before_next_attack = attack_time - datetime.now()
    if time_before_next_attack < TIME_OFFSET:
        return True

    return False


def _try_to_ghost(planet: Planet,
                  game: GameInterface,
                  my_planets: List[Planet]) -> None:
    for i in range(RETRIES_COUNT):
        # noinspection PyBroadException
        try:
            _do_ghost_to_random_planet(planet, my_planets, game)
            return
        except Exception:
            if i != RETRIES_COUNT - 1:  # If not last retry
                #  Log and retry.
                LOG.exception("Failed to ghost {} (try {}/{}).".format(planet, i + 1, RETRIES_COUNT))
            else:
                LOG.info("Giving up ghosting {}.".format(planet))
                raise CouldNotGhostException(planet)


def _pick_random_planet(my_planets: List[Planet], excluded_planet: Planet) -> Planet:
    my_planets_coords = list(map(lambda x: x.coord, my_planets))
    random_planet = random.choice(list(filter(lambda x: x != excluded_planet.coord, my_planets_coords)))
    random_planet = random_planet[1:-1]
    random_planet = random_planet.split(":") + ['PLANET']
    return random_planet


def _do_ghost_to_random_planet(planet: Planet, my_planets: List[Planet], game: GameInterface) -> None:
    destination = _pick_random_planet(my_planets, planet)
    game.ghost(planet, destination)


def _get_time_till_next_attack(hostile_missions, planet: Planet) -> timedelta:
    attacks = _get_attacks_to_this_planet(hostile_missions, planet)
    return min(map(lambda x: convert_to_timedelta(x.time1), attacks))


def _get_next_attack_time(hostile_missions, planet: Planet) -> datetime:
    return datetime.now() + _get_time_till_next_attack(hostile_missions, planet)


def _get_attacks_to_this_planet(hostile_missions, planet: Planet) -> List[str]:
    a = filter(lambda x: x.dst == planet.coord, hostile_missions)
    return list(a)


def _get_planets_being_under_attacks(hostile_missions, my_planets):
    planets_under_attack = set(map(lambda x: x.dst, hostile_missions))
    my_planets = filter(lambda x: x.coord in planets_under_attack, my_planets)
    return list(my_planets)


def _get_ghost_missions(friendly_missions):
    ghost_missions = filter(lambda x: x.mission == 'Stationner', friendly_missions)
    ghost_missions = filter(lambda x: x.time2, ghost_missions)  # Just missions that can be canceled.
    return ghost_missions
