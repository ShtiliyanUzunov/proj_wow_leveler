import time

import numpy as np
import pyautogui
from PIL     import Image

from constants import cast_pixel_avg
from state.state import state
from util import save_dbg_img, get_vector_angle

cast_image = Image.open('assets/castbar.png')
cast_image = np.array(cast_image)

def cast_water_shield():
    print("Casting water shield")
    pyautogui.press('f')
    pyautogui.sleep(1.5)


def cast_healing_wave():
    print("Casting healing wave")
    pyautogui.press('e')
    pyautogui.sleep(3.4)

def cast_flame_shock():
    print("Casting flame shock")
    pyautogui.press('3')
    pyautogui.sleep(1.5)

def drink_water():
    print("Drinking water")
    pyautogui.press('`')
    state['isDrinking'] = True
    state['drinkStarted'] = time.time()


def cast_lightning_bolt():
    pyautogui.press('1')
    pyautogui.sleep(0.7)

    cast_img = pyautogui.screenshot(region=(856, 793, 7, 7))
    save_dbg_img(cast_img, 'debug/cast_img.png')
    cast_img = np.array(cast_img)

    not_casting_vector = np.array([150, 150, 150])
    try:
        avg_diff_vector = np.average(cast_image - cast_img, axis=(0, 1))
    except:
        print ("Casting lightning bolt - failed")
        return False

    if get_vector_angle(not_casting_vector, avg_diff_vector) > 0.2:
        print("Casting lightning bolt - failed")
        return False

    pyautogui.sleep(2)
    print("Casting lightning bolt - success")
    return True
