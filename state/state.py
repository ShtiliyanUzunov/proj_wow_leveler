import numpy as np
import pyautogui
import time

from PIL import Image
from pytesseract import pytesseract

from constants import hp_pixel_avg, mana_pixel_avg
from util import save_dbg_img, get_vector_angle

state = {
    'hp': 0,
    'mana': 0,
    'isDrinking': False,
    'drinkStarted': -1,
    'lastPositionFetch': -1,
    'position': (-1, -1),
    'hasTarget': False,
    'isInCombat': False,
    'isCharacterOk': True
}

# Load PIL image
inCombat_image = Image.open('assets/inCombat.png')
inCombat_image = np.array(inCombat_image)


def is_in_combat():
    combat_status_img = pyautogui.screenshot(region=(28, 94, 25, 23))
    save_dbg_img(combat_status_img, 'debug/combat_status.png')
    combat_status_img = np.array(combat_status_img)

    not_in_combat_vector = np.array([150, 150, 150])
    avg_diff_vector = np.average(inCombat_image - combat_status_img, axis=(0, 1))

    if np.sum(avg_diff_vector) < 50:
        return True

    return False


def try_to_get_player_position():
    pyautogui.press('m')

    pyautogui.sleep(1)

    x = None
    y = None

    try:
        coord_all = pyautogui.screenshot(region=(700, 29, 500, 19))
        save_dbg_img(coord_all, 'debug/coord_all.png')
        coord_string = pytesseract.image_to_string(coord_all)
        coord_string = coord_string[coord_string.index("Player.") + len("Player."):].replace("\n", "")

        print(coord_string)

        coord_string = coord_string.replace('X', '')
        coord_string = coord_string.replace('x', '')
        coord_string = coord_string.replace('Y', '')
        coord_string = coord_string.replace('y', '')
        coord_string = coord_string.replace(' ', '')

        # Smart Tesserract is NOT! smart...
        coord_string = coord_string.replace('O', '0')
        coord_string = coord_string.replace('o', '0')
        coord_string = coord_string.replace('I', '1')
        coord_string = coord_string.replace('l', '1')
        coord_string = coord_string.replace('Z', '2')
        coord_string = coord_string.replace('z', '2')
        coord_string = coord_string.replace('B', '3')
        coord_string = coord_string.replace('b', '3')
        coord_string = coord_string.replace('A', '4')
        coord_string = coord_string.replace('S', '5')

        x = float(coord_string.split(',')[0])
        y = float(coord_string.split(',')[1])

        print("x: " + str(x) + " y: " + str(y))
    except:
        pass

    pyautogui.press('m')

    return x, y


def get_hp_and_mana():
    # Coordinates are: left, top, width, height
    bar_width = 136
    location_hp_bar = (108, 77, bar_width, 13)
    location_mana_bar = (108, 90, bar_width, 13)

    hp_bar = pyautogui.screenshot(region=location_hp_bar)
    mana_bar = pyautogui.screenshot(region=location_mana_bar)

    save_dbg_img(hp_bar, 'debug/hp_bar.png')
    save_dbg_img(mana_bar, 'debug/mana_bar.png')

    # Convert PIL image to NP array
    hp_bar = np.array(hp_bar)
    mana_bar = np.array(mana_bar)

    hp_total_pixels = 0

    for i in range(0, hp_bar.shape[1]):
        angle = get_vector_angle(hp_pixel_avg, hp_bar[7, i])
        if (angle > 0.1):
            break
        hp_total_pixels += 1

    mana_total_pixels = 0

    for i in range(0, mana_bar.shape[1]):
        angle = get_vector_angle(mana_pixel_avg, mana_bar[7, i])
        if (angle > 0.1):
            break
        mana_total_pixels += 1

    hp_total = hp_total_pixels / bar_width
    mana_total = mana_total_pixels / bar_width

    return hp_total, mana_total


def update_state():
    print("Updating state...")
    state['hp'], state['mana'] = get_hp_and_mana()
    state['isCharacterOk'] = state['hp'] > 0.4 and state['mana'] > 0.25
    state['isInCombat'] = is_in_combat()

    if state['lastPositionFetch'] == -1 or (time.time() - state['lastPositionFetch'] > 30 and not state['isInCombat']):
        state['position'] = try_to_get_player_position()
        state['lastPositionFetch'] = time.time()
        pass
