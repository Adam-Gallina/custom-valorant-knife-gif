I do not claim ownership of the gifs in `./Test Gifs/`, I found those in various holes of the internet and thought they were funny or good to test with

To run: Start `custom_val_gif.py`...and then just play val. It will be slightly inaccurate given that the software has no idea if you have your knife out or not, but it attempts to guess based on input - just scroll up violently if you're trying to inspect your knife and nothing happens

`resize_gif.py`: Tool to preprocess/resize the gifs

`val_handler.py`: Controls when to play an animation, attempts to guess when your knife is out

TODO:
 * Add json file to contain settings (change key binds, etc)
 * Root tkinter window allows you to set up gifs (change gif locations, size, speed, etc)
 * Support custom animations for more than just the knife