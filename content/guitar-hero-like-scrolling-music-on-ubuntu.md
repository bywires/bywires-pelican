Title: Guitar Hero-like scrolling music on Ubuntu
Date: 2011-08-02 13:00
Author: Admin
Category: using-software
Tags: drums, linux, midi, music, playonlinux, synthesia, ubuntu, wine

This year I began to learn to play the drums. Its been fun but I am not
the most dedicated student. Its a hobby and I slack off a lot, but I
really would like to get better.

I first got interested in the drums when I tried them out on Guitar
Hero. It was fun playing with friends and you could play for hours
without thinking about it. You'd see yourself getting better and more
comfortable. You'd notice what got tired or sore after playing for 3
hours so you'd adjust or do some Google-ing and find out how *real*
drummers do it.

Guitar Hero certainly doesn't have the capacity to teach you like a
human teacher could. It doesn't how the technique you play with, and
that's a biggy. On the other hand, real teachers cost money and
scheduled time, which at this point in my life is more than I want to
give. Over the weekend I set out on a hunt for something like Guitar
Hero with a few extra requirements.

-   Work with a Alesis DM6 electric drum kit
-   Runs on Ubuntu
-   Can load songs of a format which can be easily found for free online
    (ex. MIDI)
-   Scrolls music vertically (like Guitar Hero)
-   Rates your ability to play with the song (like Guitar Hero)

(Note: I realize some electric kits can be connected to Guitar Hero
directly but mine cannot. It has a USB-out, not MIDI-out.)

## Synthesia via PlayOnLinux

My search brought me through a graveyard of abandoned projects but
eventually I found [Synthesia][]. Synthesia, as advertised, is *almost*
what I want. Its actually made for learning/practicing piano, but it
works off MIDI tracks, so theoretically it can work with other
instruments as well.

Synthesia does not have an official Linux version. There is a forked
Linux version, [Linthesia][], but it doesn't have a 64-bit version and
[Synthesia's wiki noted it was old and missing features][]. For a while
I dug through discussion forums talking about how they managed to get
Synthesia to work with [Wine][], but experiences seemed to vary and
honestly I didn't want to dig in that deep.

Luckily I ended up stumbling upon the [PlayOnLinux][] which, just by
chance, [added support for Synthesia two weeks ago][]. PlayOnLinux is a
tool which quickly configures Wine for many Windows games and
applications. I followed the Natty [installation instructions][] and got
PlayOnLinux installed without any issue. I then followed [these
instructions][] to install a PlayOnLinux application, in this case
Synthesia. Lastly, I tweaked the Wine settings through PlayOnLinux to
have Synthesia run in "windowed" mode by following [these
instructions][1].

From here Synthesia worked immediately with my wife's MIDI keyboard.
Some articles suggest installing [Timidity][], which may be necessary in
some use cases but not for mine. I simply had the keyboard input set to
the MIDI keyboard, and the output also set to the MIDI keyboard. I had
installed Timidity but it didn't seem to be necessary and it crashed
once for me so I removed it.

## Is that it for drumming with Synthesia?

No.

This is where I've left off. Synthesia registers my drum hits and can
output to my drum kit. I tried downloading MIDI files with percussion
tracks and tried playing a long. None of my hits seemed to match the
drums Synthesia wanted me to hit. I believe this is a MIDI note mapping
mismatch. For example, my snare drum produces note 38, says
[QMidiRoute][]. I suspect the MIDI track I was playing to did not have
the snare drum sound as being note 38. Overall I'm not really familiar
with MIDI at all so this could be a completely ignorant assessment but
for now its what I'm working on. When/If I find a good solution I will
post it.

[Synthesia]: http://synthesiagame.com/
[Linthesia]: http://sourceforge.net/projects/linthesia/
[Synthesia's wiki noted it was old and missing features]: http://www.synthesiagame.com/wiki/Linux_version
[Wine]: http://www.winehq.org/
[PlayOnLinux]: http://www.playonlinux.com/
[added support for Synthesia two weeks ago]: http://www.playonlinux.com/en/commentaires-925.html
[installation instructions]: http://www.playonlinux.com/en/download.html
[these instructions]: http://www.playonlinux.com/en/manual.html
[1]: http://www.synthesiagame.com/wiki/Resources_Manual#Linux_version
[Timidity]: http://timidity.sourceforge.net/
[QMidiRoute]: http://alsamodular.sourceforge.net/
