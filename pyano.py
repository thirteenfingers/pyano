#!/usr/bin/env python

from scipy.io import wavfile
from os.path import exists
import re
import pygame

# keep the config file wherever, just update this line accordingly
configfile = "/home/ben/devel/pyano/.pyanoconfig"

# parses config file if it exists and return dictionary (empty on failure)
# assumes config file is of form:
# field:value
# field:value
# etc.
def getconfig(cfgfile):
    configinfo = {}
    if exists(cfgfile):
        configlist = re.split('\n', open(cfgfile).read().strip())
        configinfo = dict([ re.split(':', ln, 1) for ln in configlist ])
    return configinfo

# assuming the directory at "libpath" contains 88 wav files plus the plaintext
#   notelist file, this returns a tuple (bit_rate, list_of_wav_objects)
# note to self: add error checking
def getnotes(libpath):
    notelist = open(libpath + "notelist").read().strip().split('\n')
    notepairs = [ (wavfile.read(libpath + n)) for n in notelist ]
    fps, note = notepairs[0]
    return (fps, [ n for (f, n) in notepairs ])

# colors used
colors = {'white' : (255, 255, 255),
          'downwhite' : (191, 191, 191),
          'black' : (32, 32, 32),
          'downblack' : (64, 64, 64)}

# complete map of where keys are
# num -> (color, [rect1, rect2ifnecessary])
# white key = 35 pixels across (including 1 pixel border)
# black key (of 2) = 21
# black key (of 3) = 20
# 22 white keys = 22 * 35 = 770
# 
# there's probably a more elegant way of doing this than hard-coding all the
#   Rect objects
keyrects = {
    0 : ('white', [pygame.Rect(1, 1, 19, 89),
                   pygame.Rect(1, 90, 33, 59)]),
    1 : ('black', [pygame.Rect(22, 1, 19, 88)]),
    2 : ('white', [pygame.Rect(43, 1, 19, 89),
                   pygame.Rect(36, 90, 33, 59)]),
    3 : ('black', [pygame.Rect(64, 1, 19, 88)]),
    4 : ('white', [pygame.Rect(85, 1, 19, 89),
                   pygame.Rect(71, 90, 33, 59)]),
    5 : ('white', [pygame.Rect(106, 1, 18, 89),
                   pygame.Rect(106, 90, 33, 59)]),
    6 : ('black', [pygame.Rect(126, 1, 18, 88)]),
    7 : ('white', [pygame.Rect(146, 1, 18, 89),
                   pygame.Rect(141, 90, 33, 59)]),
    8 : ('black', [pygame.Rect(166, 1, 18, 88)]),
    9 : ('white', [pygame.Rect(186, 1, 18, 89),
                   pygame.Rect(176, 90, 33, 59)]),
    10 : ('black', [pygame.Rect(206, 1, 18, 88)]),
    11 : ('white', [pygame.Rect(226, 1, 18, 89),
                   pygame.Rect(211, 90, 33, 59)]),
    12 : ('white', [pygame.Rect(1 + 245, 1, 19, 89),
                   pygame.Rect(1 + 245, 90, 33, 59)]),
    13 : ('black', [pygame.Rect(22 + 245, 1, 19, 88)]),
    14 : ('white', [pygame.Rect(43 + 245, 1, 19, 89),
                   pygame.Rect(36 + 245, 90, 33, 59)]),
    15 : ('black', [pygame.Rect(64 + 245, 1, 19, 88)]),
    16 : ('white', [pygame.Rect(85 + 245, 1, 19, 89),
                   pygame.Rect(71 + 245, 90, 33, 59)]),
    17 : ('white', [pygame.Rect(106 + 245, 1, 18, 89),
                   pygame.Rect(106 + 245, 90, 33, 59)]),
    18 : ('black', [pygame.Rect(126 + 245, 1, 18, 88)]),
    19 : ('white', [pygame.Rect(146 + 245, 1, 18, 89),
                   pygame.Rect(141 + 245, 90, 33, 59)]),
    20 : ('black', [pygame.Rect(166 + 245, 1, 18, 88)]),
    21 : ('white', [pygame.Rect(186 + 245, 1, 18, 89),
                   pygame.Rect(176 + 245, 90, 33, 59)]),
    22 : ('black', [pygame.Rect(206 + 245, 1, 18, 88)]),
    23 : ('white', [pygame.Rect(226 + 245, 1, 18, 89),
                   pygame.Rect(211 + 245, 90, 33, 59)]),
    24 : ('white', [pygame.Rect(1 + 490, 1, 19, 89),
                   pygame.Rect(1 + 490, 90, 33, 59)]),
    25 : ('black', [pygame.Rect(22 + 490, 1, 19, 88)]),
    26 : ('white', [pygame.Rect(43 + 490, 1, 19, 89),
                   pygame.Rect(36 + 490, 90, 33, 59)]),
    27 : ('black', [pygame.Rect(64 + 490, 1, 19, 88)]),
    28 : ('white', [pygame.Rect(85 + 490, 1, 19, 89),
                   pygame.Rect(71 + 490, 90, 33, 59)]),
    29 : ('white', [pygame.Rect(106 + 490, 1, 18, 89),
                   pygame.Rect(106 + 490, 90, 33, 59)]),
    30 : ('black', [pygame.Rect(126 + 490, 1, 18, 88)]),
    31 : ('white', [pygame.Rect(146 + 490, 1, 18, 89),
                   pygame.Rect(141 + 490, 90, 33, 59)]),
    32 : ('black', [pygame.Rect(166 + 490, 1, 18, 88)]),
    33 : ('white', [pygame.Rect(186 + 490, 1, 18, 89),
                   pygame.Rect(176 + 490, 90, 33, 59)]),
    34 : ('black', [pygame.Rect(206 + 490, 1, 18, 88)]),
    35 : ('white', [pygame.Rect(226 + 490, 1, 18, 89),
                   pygame.Rect(211 + 490, 90, 33, 59)]),
    36 : ('white', [pygame.Rect(736, 1, 33, 148)])
                           }

# here begins the dirty graphics work
def drawkeyboard(img, krects):
    img.fill((0,0,0))
    for (c, rects) in krects.values():
        for r in rects:
            img.fill(colors[c], r)
    pygame.display.flip()
    return

# k is the number of the key from 0 to 36 inclusive (3 octaves + extra at top)
def depresskey(img, krects, k):
    (c, rects) = krects[k]
    newc = (0, 0, 0)
    if c == 'white':
        newc = colors['downwhite']
    if c == 'black':
        newc = colors['downblack']
    for r in rects:
        img.fill(newc, r)
        pygame.display.update(r)
    return

def releasekey(img, krects, k):
    (c, rects) = krects[k]
    for r in rects:
        img.fill(colors[c], r)
        pygame.display.update(r)
    return

# the main main main function
# takes filepath of configuration file
def runpyano(filename):

    conf = getconfig(filename)
    if (len(conf) == 0):
        print("Pyano: can't find config file")
        return

    fps, notes = getnotes(conf['libpath'])

    # set up the window and draw the keyboard
    screen = pygame.display.set_mode([770,150])
    pygame.display.set_caption("Pyano beta")
    drawkeyboard(screen, keyrects)

    # set up the audio
    pygame.mixer.init(fps, -16, 2, 128)
    keys = open(conf['keyboard']).read().split('\n')
    sounds = map(pygame.sndarray.make_sound, notes)

    # default range: starting from 2nd C from the left of an 88-key keyboard
    offset = 15

    # we have two dictionaries: key -> key number (as in on a real piano)
    # and key number -> sound
    # this makes it easy to do transposition, simply by adding or subtracting
    #   12 to raise or lower by an octave
    key_num = dict( zip(keys, range(len(keys))) )
    num_sound = dict( zip(range(len(sounds)), sounds) )

    is_key_down = {k: False for k in keys}
    is_key_caught = {k: False for k in keys}
    is_pedal_down = False

    while True:

        event =  pygame.event.wait()

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)

        if event.type == pygame.KEYDOWN:

            if (key in key_num.keys()) and (not is_key_down[key]):
                depresskey(screen, keyrects, key_num[key])
                num_sound[key_num[key]+offset].play()
                is_key_down[key] = True
                if is_pedal_down:
                    is_key_caught[key] = True

            elif event.key == pygame.K_PAGEUP and offset <= len(sounds) - len(keys):
                offset += 12
                print("Shift range UP an octave")

            elif event.key == pygame.K_PAGEDOWN and offset >= 12:
                offset -= 12
                print("Shift range DOWN an octave")

            elif event.key == pygame.K_SPACE:
                is_pedal_down = True
                print("-ENOTSUP")

            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise KeyboardInterrupt
                return

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_SPACE:
                is_pedal_down = False
                for k in keys:
                    is_key_caught[k] = False
                print("-ENOTSUP")

            elif key in key_num.keys():
                releasekey(screen, keyrects, key_num[key])
                num_sound[key_num[key]+offset].fadeout(50) # stops with 50ms fadeout
                is_key_down[key] = False

# do everything
runpyano(configfile)
