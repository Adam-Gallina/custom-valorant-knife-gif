import keyboard, time
from pynput.mouse import Listener, Button

KEY_INSPECT = ['y']
KEY_CHANGE = ['1', '2', '4']
KEY_CHANGE_EQUIP_VAL = [3, 2, 4]
KEY_UTIL = ['q', 'e', 'f', 'x']
KNIFE_VAL = 1
KEY_KNIFE = ['3']
#KEY_QUIT = ['\'']

class KnifeController():
    # Default to secondary weapon
    curr_equip = 2

    def __init__(self, startAnim, stopAnim, animOnlyOnKnife):
        self.start_anim = startAnim
        self.stop_anim = stopAnim
        self.animOnlyOnKnife = animOnlyOnKnife

    def change_curr_equip(self, val):
        if self.curr_equip == KNIFE_VAL and val != KNIFE_VAL:
            self.stop_anim()
        self.curr_equip = val

    def keyboard_thread(self):
        while True:
            lastKey = keyboard.read_key()
            if lastKey in KEY_INSPECT:
                if not self.animOnlyOnKnife or self.curr_equip == KNIFE_VAL:
                    self.start_anim()
            elif lastKey in KEY_KNIFE:
                self.change_curr_equip(1)
            elif lastKey in KEY_CHANGE:
                self.change_curr_equip(KEY_CHANGE_EQUIP_VAL[KEY_CHANGE.index(lastKey)])
            elif lastKey in KEY_UTIL:
                self.stop_anim()
            #elif lastKey in KEY_QUIT:
            #    anim.window.destroy()
            #    root.destroy()
            time.sleep(.1)

    def on_click(self, x, y, button, pressed):
        # Assume any mouse click is the user performing an anim-ending action
        self.stop_anim()

    def on_scroll(self, x, y, dx, dy):
        self.change_curr_equip(clamp(self.curr_equip - dy, 1, 3))

    def start_mouse_listener(self):
        with Listener(on_click=self.on_click, on_scroll=self.on_scroll) as listener:
            listener.join()

def clamp(val, minVal, maxVal):
    if val < minVal:
        return minVal
    elif val > maxVal:
        return maxVal
    return val