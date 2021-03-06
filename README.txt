This is a fork of Zulko's Pianoputer (https://github.com/Zulko/pianoputer) which I first learned about on Hacker News. In anticipation of traveling to places without a piano, I was intrigued by the possibility of using my laptop as a substitute.

In Zulko's original program, much of the code dealt with shifting the pitch of a single audio file to generate different pitches. As interesting as that part of the program was, I wanted to use a particular set of audio files that I found more pleasing, so I removed the pitch-shifting part of the code. I then restructured the remaining code and added a range shifting feature so that page up/page down shifts the range by an octave at a time. Then, just for fun, I added a graphical display of a piano keyboard which would highlight the piano keys corresponding to whichever computer keys I was pressing.

This is a work in progress, and there is a great deal of error checking (such as files not existing) that I haven't done yet. The keyboard size is assumed to be 37 keys (3 chromatic octaves plus an extra C), and the layout specified in my_keyboard.kb arranges the computer keys in as close to a piano-like arrangement as possible:

 s d  g h j  l ;  2 3 4  6 7  9 0 -
z x cv b n m, . /q w e rt y ui o p []

Also, I have found that certain combinations of three or more simultaneous notes may not play properly. As far as I can tell this is a hardware limitation.

*** EDIT (2014-12-22) ***

The spacebar now acts as the sustain pedal. Also, since I apparently forgot to mention it earlier, you hit 'escape' to quit.

While implementing the spacebar-pedal I discovered it was easiest to rip out the innards of the original program and rewrite it in a more object-oriented fashion; Keys and Notes are now objects with pointers to each other. It is my hope that this new workalike version will also facilitate the development of other features.

