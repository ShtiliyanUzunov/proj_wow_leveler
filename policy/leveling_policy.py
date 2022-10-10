import time
import random

from actions.positioning import turn_n_degrees, walk_forward_n_seconds
from actions.spells import cast_lightning_bolt, cast_healing_wave, drink_water, cast_water_shield, cast_flame_shock
from state.state import state, is_in_combat
from actions.targeting import search_for_target_forward, try_to_mark_target_with_tab, remove_target

r = random.Random()


def ensure_character_is_ok():
    if state['isCharacterOk']:
        return

    if state['mana'] < 0.25:
        if not state['isInCombat']:
            if not state['isDrinking']:
                drink_water()
        else:
            cast_water_shield()

    if state['hp'] < 0.55:
        cast_healing_wave()


def continue_drinking_if_drinking():
    if state['isInCombat']:
        state['isDrinking'] = False
        return False

    if state['isDrinking']:
        if time.time() - state['drinkStarted'] > 20:
            state['isDrinking'] = False
            print("Stop drink. Too much time passed.")
            return False

        print("Continue drinking.")
        return True

    state['isDrinking'] = False
    return False


def apply_leveling_policy():
    if continue_drinking_if_drinking():
        return

    ensure_character_is_ok()

    if state['isInCombat']:
        print("In combat")
        success = cast_lightning_bolt()

        if not success:
            for i in range(0, 4):
                turn_n_degrees(90)
                success = cast_lightning_bolt()

                if not is_in_combat():
                    return

                if success:
                    break
    else:
        print("Not in combat")
        if state['isDrinking']:
            return

        remove_target()
        turn_n_degrees(r.randint(0, 360))
        if search_for_target_forward():
            cast_flame_shock()
            result = cast_lightning_bolt()

            if not result:
                for i in range(0, 3):
                    walk_forward_n_seconds(1)
                    cast_flame_shock()
                    if cast_lightning_bolt():
                        break
