from directkeys import *

paused = True
debounce = 0

while True:
    if not paused:
        print('play')
        #PressKey('S')
        mouseUp('right')
        mouseDown('right')

    if getKey('Z') and getKey('X') and time.time() - debounce > 0.5:
        paused = not paused
        debounce = time.time()
        if paused:
            ReleaseKey('S')
            mouseUp('right')