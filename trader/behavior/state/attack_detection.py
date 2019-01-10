import random
from datetime import timedelta

from trader.behavior.context import Context
from trader.behavior.game_state import GameState
from trader.behavior.state.sleep import Sleep
from trader.interface.constants import MAX_TIME_MINUTES, MIN_TIME_MINUTES
from trader.interface.screen.fleet import FleetScreen
from trader.interface.screen.fleet_info import FleetInfoScreen
from trader.interface.screen.generic_screen import Planet
from trader.util.log import LOG
from trader.util.util import convert_to_timedelta

TIME_OFFSET = timedelta(minutes=5)


def _ghost_to_random_planet(ctx, planet, my_planets):
    # Pick a random planet to ghost.
    MY_PLANETS_COORDS = list(map(lambda x: x.coord, my_planets))
    destination = random.choice(list(filter(lambda x: x != planet.coord, MY_PLANETS_COORDS)))
    destination = destination[1:-1]
    destination = destination.split(":") + ['PLANET']

    with FleetScreen(ctx.driver) as screen:
        screen.select_planet(planet)
        screen.ghost_all(destination)


def _get_next_attack(hostile_missions, planet):
    attacks = _get_attacks_to_this_planet(hostile_missions, planet)
    return min(map(lambda x: convert_to_timedelta(x.time1), attacks))


def _get_attacks_to_this_planet(hostile_missions, planet):
    a = filter(lambda x: x.dst == planet, hostile_missions)
    return list(a)


class AttackDetection(GameState):

    def run(self, ctx: Context) -> GameState:
        ctx.sleep_for = timedelta(minutes=random.randint(MIN_TIME_MINUTES, MAX_TIME_MINUTES))

        # Get fleet information.
        with FleetInfoScreen(ctx.driver) as screen:
            my_planets = screen.extract_planets()
            missions = screen.extract_info()

        # Extract relevant pieces of information.
        hostile_missions = missions["hostile"]
        friendly_missions = missions["friendly"]

        # Ghost fleet on every threatened planet.
        for planet in set(map(lambda x: x.dst, hostile_missions)):
            try:
                time_before_next_attack = _get_next_attack(hostile_missions, planet)
                if time_before_next_attack < TIME_OFFSET:
                        LOG.debug("Someone is attacking {}, ghosting everything...".format(planet.name))
                        _ghost_to_random_planet(ctx, planet, my_planets)
                        ctx.sleep_for = min(ctx.sleep_for, time_before_next_attack + TIME_OFFSET)
                else:
                    ctx.sleep_for = min(ctx.sleep_for, time_before_next_attack - TIME_OFFSET)
                    log_msg = "Someone is attacking {} but we still have time ({}) to sleep..."
                    LOG.debug(log_msg.format(planet.name, time_before_next_attack))
            except Exception:
                LOG.exception("Failed to ghost {}".format(planet))  #  Log and ghost other planets.

        # Order ghost fleet to come back if the planet is safe.
        ghost_missions = filter(lambda x: x.mission == 'Stationner', friendly_missions)
        ghost_missions = filter(lambda x: x.time2, ghost_missions)
        for mission in ghost_missions:
            attacks = _get_attacks_to_this_planet(hostile_missions, mission.src)
            if not attacks:
                with FleetInfoScreen(ctx.driver) as screen:
                    screen.select_planet(mission.src)
                with FleetInfoScreen(ctx.driver) as screen:
                    LOG.info("{} is safe, retrieving ghost fleet.".format(mission.src))
                    screen.order_come_back(mission.src)
            else:
                LOG.info("{} is still threatened.".format(mission.src))

        return Sleep(self, 30)


attackDetection = AttackDetection()
