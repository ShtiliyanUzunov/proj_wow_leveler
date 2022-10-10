import pyautogui


def walk_forward_n_seconds(n):
    print("Walking forward for " + str(n) + " seconds")
    pyautogui.keyDown('w')
    pyautogui.sleep(n)
    pyautogui.keyUp('w')


def turn_n_degrees(n):
    print("Turning " + str(n) + " degrees")
    pyautogui.keyDown(']')

    # Epirically determined...
    sleep_seconds = n / 203
    pyautogui.sleep(sleep_seconds)
    pyautogui.keyUp(']')
