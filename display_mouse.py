# mouseNow.py - Displays the mouse cursor's current position.

# preliminary
import pyautogui, time
pyautogui.PAUSE = .001
pyautogui.FAILSAFE = True

print('Press Ctrl-C to quit.')


try:
    x, y = pyautogui.position()
    positionStr = "X: " + str(x).rjust(4) + " Y: " + str(y).rjust(4)
    print(positionStr, end='')
    print('\r')

    while True:
        if pyautogui.position() != (x, y) :
            x, y = pyautogui.position()
            positionStr = "X: " + str(x).rjust(4) + " Y: " + str(y).rjust(4)
            print(positionStr, end='')
            print('\r')
            #print('\b' * len(positionStr), end='', flush=True)

except KeyboardInterrupt:
    print('\nDone.')
