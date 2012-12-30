Title: Streaming Spotify from OS X to XBMC on a Raspberry Pi using Soundflower, LadioCast, and Icecast
Date: 2012-12-08 14:48
Author: Admin
Category: using-software
Tags: audio, homebrew, icecast, ladiocast, linux, music, nicecast, raspberry pi, soundflower, streaming

My Goal here was pretty simple: Play [Spotify][] on my [Raspberry Pi][]
running [XBMC][]. The easiest and most usable way to do this would be to
install something like the [Spotimc][] plugin in XBMC itself. Spotimc,
like all 3rd party Spotify libraries at the moment, seems to require a
Spotify Premium account. If you, like me, aren't ready to spend $10 a
month for the service then read on.

The next option I considered was streaming from my Spotify desktop
client on my laptop running OS X to XBMC. XBMC can play a [PLS file][]
without any extra plugins installed so I rolled with that. I just needed
to create a stream from my laptop running OS X which the PLS file would
point to.

For $59 you can do this in a couple of seconds using [Nicecast][]. I
didn't want to spend $59 so I continued on my quest for *free*.

Here are some brief descriptions of the software you're going to use:

Soundflower
:   "Soundflower is a MacOS system extension that allows applications to
    pass audio to other applications." It allows you to treat your
    system sound like an audio source in other applications, in this
    case LadioCast.
Icecast
:   "Icecast is free server software for streaming multimedia." It
    serves streaming audio.
LadioCast
:   "LadioCast is a software running on Mac OS X to stream digital audio
    such as Internet radio program." It functions as an audio source for
    your Icecast server.

## Streaming audio from OS X

1.  Install [Soundflower][]
2.  System Preferences \> Sound \> Output \> Soundflower (2ch)
3.  Install [Icecast][] using [Homebrew][]: *brew install icecast*
4.  Run icecast: *icecast -c
    /usr/local/Cellar/icecast/2.3.3/etc/icecast.xml*
5.  Get your network IP: Open terminal \> *ifconfig en0 | grep "inet " |
    cut -d" " -f 2*
6.  Install [LadioCast][]
7.  Launch and configure LadioCast
    -   Input 1 \> Soundflower (2ch)
    -   Streamer \> Stream 1 \> Icecast
        -   Connection
            -   Host \> Your network IP
            -   Port \> 8000
            -   Mount \> /stream
            -   User \> source
            -   Password \> hackme
        -   Encoding
            -   Format \> Ogg Vorbis
            -   Bit Rate Mode \> Variable
            -   Quality Level \> 2
        -   Click "connect"
8.  Play some music from Spotify (continuously loop it for testing
    purposes)

## Receiving streaming audio on Rasperry Pi with XBMC

Create PLS file in a directory you can access from XBMC.

    [playlist]
    File1=http://YOUR_MACS_IP:8000/stream
    Title1=My Stream
    Length1=-1
    Version=2

Then from XBMC \> Music \> Files, browse to the PLS file and "play" it.

After a few seconds you should hear your music. If its choppy, like mine
was initially, try tweaking the *Quality Level* setting in your
LadioCast Icecast stream settings.

Enjoy!

[Spotify]: http://www.spotify.com
  [Raspberry Pi]: http://www.raspberrypi.org/
  [XBMC]: http://xbmc.org/
  [Spotimc]: https://github.com/mazkolain/spotimc
  [PLS file]: http://en.wikipedia.org/wiki/PLS_(file_format)
  [Nicecast]: http://www.rogueamoeba.com/nicecast/
  [Soundflower]: http://code.google.com/p/soundflower/
  [Icecast]: http://www.icecast.org/
  [Homebrew]: http://mxcl.github.com/homebrew/
  [LadioCast]: https://itunes.apple.com/us/app/ladiocast/id411213048?mt=12
