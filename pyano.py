#!/usr/bin/env python

from scipy.io import wavfile
from os.path import exists
import re
import pygame

# keep the config file wherever, just update this line accordingly
configfile = "/home/ben/devel/pyano/.pyanoconfig"

# colors used
colors = {'white' : (255, 255, 255),
          'downwhite' : (191, 191, 191),
          'black' : (32, 32, 32),
          'downblack' : (64, 64, 64)}

# Note is a wrapper class for one of the 88 sounds
class Note:

    def __init__(self, snd):
        self.sound = snd
        self.playing = False
        self.caught = False # for sustain pedal
        self.key = None

    def play(self):
        if self.playing:
            self.sound.fadeout(50)
        self.sound.play()
        self.playing = True

    def stop(self):
        self.sound.fadeout(50)
        self.playing = False

    def catch(self):
        self.caught = True

    def uncatch(self):
        self.caught = False
        if (self.key is None):
            self.stop()
        elif not(self.key.is_down()):
            self.stop()

    def is_caught(self):
        return self.caught

    def get_key(self):
        return self.key

    def set_key(self, k):
        self.key = k

# a PianoKey corresponds to one of the keyboard keys displayed on the screen
class PianoKey():

    # n : Note object
    # i : index from 0 to 36 of the 3-octave keyboard
    # img : the pygame screen
    # c_dc_rects : entry from the keyrects list -
    #       tuple containing color, down-color, list of pygame.Rect objects
    def __init__(self, n, i, img, c_dc_rects):
        self.note = n
        self.note.set_key(self) # backward pointer
        self.next_note = n # placeholder for range shifts
        self.down = False
        self.index = i
        self.img = img
        (c, dc, rects) = c_dc_rects
        self.rects = rects
        self.color = colors[c]
        self.downcolor = colors[dc]

    def press(self):
        self.down = True
        self.note.play()
        for r in self.rects:
            self.img.fill(self.downcolor, r)
            pygame.display.update(r)

    def release(self):
        self.down = False
        if not(self.note.is_caught()):
            self.note.stop()
        # if no other key is pointing to this note already
        if (self.note.get_key() == self):
            self.note.set_key(None)
        self.note = self.next_note
        self.note.set_key(self)
        for r in self.rects:
            self.img.fill(self.color, r)
            pygame.display.update(r)

    def update(self, n):
        self.next_note = n
        if not(self.down):
            n.set_key(self)
            # if no other key is pointing to this note already
            if (self.note.get_key() == self):
                self.note.set_key(None)
            self.note = n

    def get_index(self):
        return self.index

    def is_down(self):
        return self.down

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
def getwavs(libpath):
    wavlist = open(libpath + "notelist").read().strip().split('\n')
    wavpairs = [ (wavfile.read(libpath + w)) for w in wavlist ]
    if len(wavpairs) != 88:
        raise Exception('Wrong number of notes! ' + len(wavpairs) + ' instead of 88')
    fps, wav = wavpairs[0]
    return (fps, [ n for (f, n) in wavpairs ])

# complete map of where keys are
# num -> (color, downcolor, [rect1, rect2ifnecessary])
# white key = 35 pixels across (including 1 pixel border)
# black key (of 2) = 21
# black key (of 3) = 20
# 22 white keys = 22 * 35 = 770
# 
# there's probably a more elegant way of doing this than hard-coding all the
#   Rect objects
keyrects = {
    0 : ('white', 'downwhite', [pygame.Rect(1, 1, 19, 89),
                                pygame.Rect(1, 90, 33, 59)]),
    1 : ('black', 'downblack', [pygame.Rect(22, 1, 19, 88)]),
    2 : ('white', 'downwhite', [pygame.Rect(43, 1, 19, 89),
                                pygame.Rect(36, 90, 33, 59)]),
    3 : ('black', 'downblack', [pygame.Rect(64, 1, 19, 88)]),
    4 : ('white', 'downwhite', [pygame.Rect(85, 1, 19, 89),
                                pygame.Rect(71, 90, 33, 59)]),
    5 : ('white', 'downwhite', [pygame.Rect(106, 1, 18, 89),
                                pygame.Rect(106, 90, 33, 59)]),
    6 : ('black', 'downblack', [pygame.Rect(126, 1, 18, 88)]),
    7 : ('white', 'downwhite', [pygame.Rect(146, 1, 18, 89),
                                pygame.Rect(141, 90, 33, 59)]),
    8 : ('black', 'downblack', [pygame.Rect(166, 1, 18, 88)]),
    9 : ('white', 'downwhite', [pygame.Rect(186, 1, 18, 89),
                                pygame.Rect(176, 90, 33, 59)]),
    10 : ('black', 'downblack', [pygame.Rect(206, 1, 18, 88)]),
    11 : ('white', 'downwhite', [pygame.Rect(226, 1, 18, 89),
                                 pygame.Rect(211, 90, 33, 59)]),
    12 : ('white', 'downwhite', [pygame.Rect(1 + 245, 1, 19, 89),
                                 pygame.Rect(1 + 245, 90, 33, 59)]),
    13 : ('black', 'downblack', [pygame.Rect(22 + 245, 1, 19, 88)]),
    14 : ('white', 'downwhite', [pygame.Rect(43 + 245, 1, 19, 89),
                                 pygame.Rect(36 + 245, 90, 33, 59)]),
    15 : ('black', 'downblack', [pygame.Rect(64 + 245, 1, 19, 88)]),
    16 : ('white', 'downwhite', [pygame.Rect(85 + 245, 1, 19, 89),
                                 pygame.Rect(71 + 245, 90, 33, 59)]),
    17 : ('white', 'downwhite', [pygame.Rect(106 + 245, 1, 18, 89),
                                 pygame.Rect(106 + 245, 90, 33, 59)]),
    18 : ('black', 'downblack', [pygame.Rect(126 + 245, 1, 18, 88)]),
    19 : ('white', 'downwhite', [pygame.Rect(146 + 245, 1, 18, 89),
                                 pygame.Rect(141 + 245, 90, 33, 59)]),
    20 : ('black', 'downblack', [pygame.Rect(166 + 245, 1, 18, 88)]),
    21 : ('white', 'downwhite', [pygame.Rect(186 + 245, 1, 18, 89),
                                 pygame.Rect(176 + 245, 90, 33, 59)]),
    22 : ('black', 'downblack', [pygame.Rect(206 + 245, 1, 18, 88)]),
    23 : ('white', 'downwhite', [pygame.Rect(226 + 245, 1, 18, 89),
                                 pygame.Rect(211 + 245, 90, 33, 59)]),
    24 : ('white', 'downwhite', [pygame.Rect(1 + 490, 1, 19, 89),
                                 pygame.Rect(1 + 490, 90, 33, 59)]),
    25 : ('black', 'downblack', [pygame.Rect(22 + 490, 1, 19, 88)]),
    26 : ('white', 'downwhite', [pygame.Rect(43 + 490, 1, 19, 89),
                                 pygame.Rect(36 + 490, 90, 33, 59)]),
    27 : ('black', 'downblack', [pygame.Rect(64 + 490, 1, 19, 88)]),
    28 : ('white', 'downwhite', [pygame.Rect(85 + 490, 1, 19, 89),
                                 pygame.Rect(71 + 490, 90, 33, 59)]),
    29 : ('white', 'downwhite', [pygame.Rect(106 + 490, 1, 18, 89),
                                 pygame.Rect(106 + 490, 90, 33, 59)]),
    30 : ('black', 'downblack', [pygame.Rect(126 + 490, 1, 18, 88)]),
    31 : ('white', 'downwhite', [pygame.Rect(146 + 490, 1, 18, 89),
                                 pygame.Rect(141 + 490, 90, 33, 59)]),
    32 : ('black', 'downblack', [pygame.Rect(166 + 490, 1, 18, 88)]),
    33 : ('white', 'downwhite', [pygame.Rect(186 + 490, 1, 18, 89),
                                 pygame.Rect(176 + 490, 90, 33, 59)]),
    34 : ('black', 'downblack', [pygame.Rect(206 + 490, 1, 18, 88)]),
    35 : ('white', 'downwhite', [pygame.Rect(226 + 490, 1, 18, 89),
                                 pygame.Rect(211 + 490, 90, 33, 59)]),
    36 : ('white', 'downwhite', [pygame.Rect(736, 1, 33, 148)])
                           }

# here begins the dirty graphics work
def drawkeyboard(img, krects):
    img.fill((0,0,0))
    for (c, downc, rects) in krects.values():
        for r in rects:
            img.fill(colors[c], r)
    pygame.display.flip()
    return

# the main main main function
# takes filepath of configuration file
def runpyano(filename):

    conf = getconfig(filename)
    if (len(conf) == 0):
        print("Pyano: can't find config file")
        return

    fps, wavs = getwavs(conf['libpath'])
    keyboardkeys = open(conf['keyboard']).read().split('\n')

    # set up the window and draw the keyboard
    screen = pygame.display.set_mode([770,150])
    pygame.display.set_caption("Pyano beta")
    drawkeyboard(screen, keyrects)

    # set up the audio
    pygame.mixer.init(fps, -16, 2, 128)
    pygame.mixer.set_num_channels(24)
    sounds = map(pygame.sndarray.make_sound, wavs)

    # default range: starting from 2nd C from the left of an 88-key keyboard
    offset = 15

    # lists of all objects: 88 notes, 37 keys
    notes = [ Note(s) for s in sounds ]
    pianokeys = [ PianoKey(notes[i+offset],
                            i,
                            screen,
                            keyrects[i]) for i in range(len(keyrects)) ]
    key_map = dict( zip(keyboardkeys, pianokeys) )
    is_pedal_down = False
    
    while True:

        event = pygame.event.wait()

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)

        if event.type == pygame.KEYDOWN:

            # all regular piano keys
            if (key in key_map.keys()):
                key_map[key].press()

            # range shift up
            elif event.key == pygame.K_PAGEUP and offset < len(sounds) - len(pianokeys):
                offset += 12
                for pianokey in key_map.values():
                    pianokey.update(notes[pianokey.get_index() + offset])
                print("Shift range UP an octave")

            # range shift down
            elif event.key == pygame.K_PAGEDOWN and offset >= 12:
                offset -= 12
                for pianokey in key_map.values():
                    pianokey.update(notes[pianokey.get_index() + offset])
                print("Shift range DOWN an octave")

            # sustain pedal
            elif event.key == pygame.K_SPACE:
                # do shit
                is_pedal_down = True
                for note in notes:
                    note.catch()
                print("Ped.")

            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise KeyboardInterrupt
                return

        elif event.type == pygame.KEYUP:
       
            # regular piano keys
            if key in key_map.keys():
                key_map[key].release()

            # sustain pedal
            elif event.key == pygame.K_SPACE:
                # do shit
                is_pedal_down = False
                for note in notes:
                    note.uncatch()
                print("*")

# do everything
runpyano(configfile)
