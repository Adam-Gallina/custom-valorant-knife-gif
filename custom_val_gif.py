from tkinter import *
from PIL import ImageTk, Image
import ctypes
import threading
from pynput.mouse import Listener

from resize_gif import resize_gif
from val_handler import KnifeController

GIF_NAME = './Test Gifs/rat_shake.gif'
IMAGE_SCALE = 2
# How long to play the animation for when inspecting (-1 for unlimited animation)
ANIM_DURATION = -1
ANIM_SPEED = 1.5
# Offsets the gif placement, anchored on the bottom right corner of the screen
IMAGE_OFFSET = (-400, 0)
ANIM_ONLY_ON_KNIFE = True


class Anim:
    isPlaying = False
    currFrame = 0
    playbackTime = 0

    def __init__(self, imagePath, imageScale, imageOffset, duration, playbackSpeed, root, screensize):
        self.duration = duration
        self.playbackSpeed = playbackSpeed

        im = Image.open(imagePath)
        imageSize = (int(im.size[0] * imageScale), int(im.size[1] * imageScale))

        self.durations = []
        for i in range(im.n_frames):
            im.seek(i)
            self.durations.append(im.info['duration'])
        im.close()
        
        self.frames = resize_gif(imagePath, imageSize)

        self.window = Toplevel(root)
        # Size and position the window
        self.window.geometry(f'{imageSize[0]}x{imageSize[1]}+{screensize[0] - imageSize[0] + imageOffset[0]}+{screensize[1] - imageSize[1] + imageOffset[1]}')
        # Hide image border
        self.window.overrideredirect(1)
        # Keep window above all other windows
        self.window.wm_attributes("-topmost", True)
        # Make background transparent
        self.window.wm_attributes("-transparentcolor", "white")

        self.label = Label(self.window, bg='white')
        self.label.pack()

        self.window.withdraw()

    def play_anim(self):
        if not self.isPlaying or (self.playbackTime >= self.duration and self.duration != -1):
            self.isPlaying = False
            self.window.withdraw()
            return

        self.display_frame(self.frames[self.currFrame])

        self.currFrame += 1
        if self.currFrame >= len(self.frames):
            self.currFrame = 0

        t = self.durations[self.currFrame]
        self.playbackTime += t
        self.window.after(int(t / self.playbackSpeed), self.play_anim)

    def display_frame(self, im):
        f = ImageTk.PhotoImage(im)
        self.label.image = f
        self.label.configure(image=f)

    def restart(self):
        if not self.isPlaying:
            self.currFrame = 0
            self.playbackTime = 0
            self.start()

    def start(self):
        if not self.isPlaying:
            self.isPlaying = True
            self.window.after(0, self.play_anim)
            self.window.deiconify()
    
    def stop(self):
        if self.isPlaying:
            self.isPlaying = False
            self.window.withdraw()


def load_anims(root):
    label = Label(root, text='Loading animations...')
    label.pack()

    user32 = ctypes.windll.user32
    screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    
    anim = Anim(GIF_NAME, IMAGE_SCALE, IMAGE_OFFSET, ANIM_DURATION, ANIM_SPEED, root, screensize)

    label.config(text='Ready!')

    return anim

def handle_input(anim):

    knifeCtl = KnifeController(anim.restart, anim.stop, ANIM_ONLY_ON_KNIFE)

    key_thread = threading.Thread(target=knifeCtl.keyboard_thread)
    key_thread.daemon = True
    key_thread.start()

    mouse_thread = threading.Thread(target=knifeCtl.start_mouse_listener)
    mouse_thread.daemon = True
    mouse_thread.start()


root = Tk()

def main():
    anim = load_anims(root)
    handle_input(anim)

root.after(0, main)

root.mainloop()

# Stop any active mouse listeners
Listener.stop