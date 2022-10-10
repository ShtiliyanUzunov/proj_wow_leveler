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


if __name__ == "__main__":
    main()
