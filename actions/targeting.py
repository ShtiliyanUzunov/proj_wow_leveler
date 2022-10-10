import numpy as np
import pyautogui

from actions.positioning import walk_forward_n_seconds
from constants import hp_pixel_avg
from state.state import state
from util import get_vector_angle


def try_to_mark_target_with_tab():
    pyautogui.keyDown('tab')

    pyautogui.sleep(0.1)
    hp_img = np.array(pyautogui.screenshot(region=(310, 79, 7, 7)))

    pyautogui.keyUp('tab')

    avg_pxl = np.average(hp_img, axis=(0, 1))
    if get_vector_angle(hp_pixel_avg, avg_pxl) > 0.1:
        print("Failed to mark target")
        return False

    print("Target marked")
    return True


def search_for_target_forward():
    print("Searching for target forward")
    for i in range(0, 5):
        walk_forward_n_seconds(1)
        if try_to_mark_target_with_tab():
            return True

    return False

def remove_target():
    pyautogui.press('esc')
