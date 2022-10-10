import time
import numpy as np
import pyautogui
import pytesseract

from policy.leveling_policy import apply_leveling_policy
from state.state import update_state

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def main():
    while True:
        active_window = pyautogui.getActiveWindow()
        if active_window is None or active_window.title.lower() != "world of warcraft":
            continue

        update_state()
        apply_leveling_policy()

        # ensure_character_is_ok()
        # cast_healing_wave()
        # search_for_target()
        # cast_lightning_bolt()
        # cast_water_shield()
        # try_to_mark_target_with_tab()
        # walk_forward_n_seconds(1)
        # turn_n_degrees(180)
        # get_hp_and_mana()
        # try_to_get_player_position()

if __name__ == "__main__":
    main()