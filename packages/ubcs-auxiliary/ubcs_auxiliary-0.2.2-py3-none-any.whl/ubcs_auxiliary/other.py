"""
advance Sleep functions
author: Valentyn Stadnytskyi
data: 2017 - Nov 17 2018

functions:
psleep - precision sleep takes
intsleep with inputs t, dt and interupt as a function.

The precision sleep class.
functiob:
psleep - sleep specified amount of time with sub milisecond precision
test_sleep - for testing purposes. will print how much time the code waited.
This is important for the Windows platform programs if precise wait is required.
The Windows OS has ~15-17 ms latenct - the shortest time between attentions from OS.
"""

def beep():
    from IPython.display import Audio
    sound_file = 'http://www.soundjay.com/button/beep-07.wav'
    Audio(sound_file, autoplay=True)
