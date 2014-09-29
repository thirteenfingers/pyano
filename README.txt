This is a fork of Zulko's Pianoputer (https://github.com/Zulko/pianoputer) which I first learned about on Hacker News. When writing music I prefer to work in front of a piano keyboard, and in anticipation of traveling to places without a piano, I was intrigued by the possibility of using my laptop as a substitute.

In Zulko's original program, much of the code dealt with shifting the pitch of a single audio file to generate different pitches. I removed that (so that I could use a particular set of audio files which I find more pleasing), restructured the remaining code, and added a range shifting feature so that page up/page down would shift the range by an octave at a time. Then, just for fun, I added a graphical display of a piano keyboard which would highlight the piano keys corresponding to whichever computer keys I was pressing.

This is a work in progress, and there is a great deal of error checking (such as files not existing) that I haven't done yet.

Also, I have found that certain combinations of more than three simultaneous notes may not play properly. As far as I can tell this is a hardware limitation.
