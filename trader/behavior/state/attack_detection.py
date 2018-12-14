import random
from datetime import timedelta

from trader.behavior.context import Context
from trader.behavior.game_state import GameState
from trader.behavior.state.sleep import Sleep
from trader.interface.constants import MAX_TIME_MINUTES, MIN_TIME_MINUTES
from trader.interface.screen.fleet import FleetScreen
from trader.interface.screen.fleet_info import FleetInfoScreen
from trader.util.log import LOG
from trader.util.util import convert_to_timedelta

TIME_OFFSET = timedelta(minutes=5)


def _is_an_attack(fleet_movement, my_planets_coords):
    return fleet_movement.mission == 'Attaquer' and fleet_movement.dst.coord in my_planets_coords and fleet_movement.src.coord not in my_planets_coords


class AttackDetection(GameState):

    def run(self, ctx: Context) -> GameState:
        ctx.next_sleep = timedelta(minutes=random.randint(MIN_TIME_MINUTES, MAX_TIME_MINUTES))

        with FleetInfoScreen(ctx.driver) as screen:
            planets = screen.extract_planets()
            fleet_info = screen.extract_info()

        coords = list(map(lambda x: x.coord, planets))

        attacks = filter(lambda x: _is_an_attack(x, coords), fleet_info)
        attacks = list(attacks)

        threatened_planets = set(map(lambda x: x.dst, attacks))
        for planet in threatened_planets:
            attacks_to_this_planet = list(filter(lambda x: x.dst == planet, attacks))
            min_time = min(map(lambda x: convert_to_timedelta(x.time1), attacks_to_this_planet))

            if min_time <= TIME_OFFSET or True:
                LOG.debug("Someone is attacking {}, ghosting everything...".format(planet.name))
                with FleetScreen(ctx.driver) as screen:
                    screen.select_planet(planet)
                    destination = random.choice(list(filter(lambda x: x != planet.coord, coords)))
                    destination = destination[1:-1]
                    destination = destination.split(":") + ['PLANET']

                    try:
                        screen.ghost_all(destination)
                        ctx.next_sleep = min(ctx.next_sleep, min_time + TIME_OFFSET)
                    except Exception:
                        LOG.warning("Failed to ghost {}".format(planet))
            else:
                ctx.next_sleep = min(ctx.next_sleep, min_time - TIME_OFFSET)
                LOG.debug(
                    "Someone is attacking {} but we still have time ({}) to sleep...".format(planet.name, min_time))

        ghosts = filter(lambda x: x.mission == 'Stationner', fleet_info)
        ghosts = filter(lambda x: x.time2, ghosts)

        for ghost in ghosts:
            attacks_to_this_planet = list(filter(lambda x: x.dst == ghost.src, attacks))
            if not attacks_to_this_planet:
                with FleetInfoScreen(ctx.driver) as screen:
                    screen.select_planet(ghost.src)
                with FleetInfoScreen(ctx.driver) as screen:
                    LOG.info("{} is safe, retrieving ghost fleet.".format(ghost.src))
                    screen.order_come_back(ghost.src)

        return Sleep(self, 30)


attackDetection = AttackDetection()
