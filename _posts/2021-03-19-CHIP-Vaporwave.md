---
layout: post
title: Vaporwave in Pocket C.H.I.P. Framebuffer
category: hack
tags: chip hack 100daystooffload
toc: true

comments:
  show:  true
  fediHost:  fosstodon.org
  fediusername:  ecliptik
  fediid:  105915488359029065

---

In the ever expanding ways to hack [my Pocket C.H.I.P.](https://www.ecliptik.com/Pocket-CHIP/), and my recent discovery of [Vaporwave](https://en.wikipedia.org/wiki/Vaporwave), I couldn't help but combine the two and have a looping music video device on my desktop. Note this is not running in `X`, but in the console framebuffer, which gives it more ＡＥＳＴＨＥＴＩＣＳ.

![Vaporwave in Pocket C.H.I.P](/assets/images/posts/chip_vaporwave/chip-vaporwave.png)
<figure><figcaption>NEON PALM MALL in C.H.I.P. Framebuffer</figcaption></figure>

## Required Software

The C.H.I.P. is fully upgraded to Debian Buster, and there were some oddities with getting `dpkg` sorted out, so the package installs may not work exactly as defined here but are a general guide. It's also [booting into the console framebuffer](http://www.chip-community.org/index.php/Setting_up_text_mode_on_PocketCHIP_4.3) and not `X`, so there's no desktop environment or window manager running.

The following tools are used,

- [mplayer](https://mplayerhq.hu/design7/news.html), for playback with framebuffer and armhf support
- [alsa-utils](https://github.com/alsa-project/alsa-utils), specifically `alsamixer` to control volume from console
- [youtube-dl](https://youtube-dl.org/), download video+audio from youtube
- [ffmpeg](https://ffmpeg.org/), combine video+audio from `youtube-dl`

Install packages,

```bash
$ sudo apt-get update
$ sudo apt-get install -y ffmpeg mplayer alsa-utils
```

Install `youtube-dl`,

```bash
$ sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
$ sudo chmod a+rx /usr/local/bin/youtube-dl
```

## Downloading Videos

Using `youtube-dl`, download a Vaporwave video. The Pocket C.H.I.P. is very particular about the screen resolution and codec of the video. Anything larger than the C.H.I.P. screen (480×272) will give an error, and some codecs won't play. I found the following format combination works best for video playback.

- resolution: `320x240@240p`
- container: `mp4`
- codec: `avc1`

For this example we'll save [NEON PALM MALL (Vaporwave Mix + Video)](https://www.youtube.com/watch?v=FZUfiW3W1KY).

First, use the `-F` argument to display the list of available formats and choose the one that best matches,

```bash
$ youtube-dl -F https://www.youtube.com/watch?v=FZUfiW3W1KY
[youtube] FZUfiW3W1KY: Downloading webpage
[info] Available formats for FZUfiW3W1KY:
format code  extension  resolution note
249          webm       audio only tiny   48k , webm_dash container, opus @ 48k (48000Hz), 18.74MiB
250          webm       audio only tiny   64k , webm_dash container, opus @ 64k (48000Hz), 24.76MiB
251          webm       audio only tiny  127k , webm_dash container, opus @127k (48000Hz), 48.90MiB
140          m4a        audio only tiny  129k , m4a_dash container, mp4a.40.2@129k (44100Hz), 49.55MiB
394          mp4        192x144    144p   51k , mp4_dash container, av01.0.00M.08@  51k, 25fps, video only, 19.82MiB
160          mp4        192x144    144p   53k , mp4_dash container, avc1.4d400b@  53k, 25fps, video only, 20.33MiB
278          webm       192x144    144p   67k , webm_dash container, vp9@  67k, 25fps, video only, 25.81MiB
133          mp4        320x240    240p   93k , mp4_dash container, avc1.4d400d@  93k, 25fps, video only, 35.73MiB
395          mp4        320x240    240p  106k , mp4_dash container, av01.0.00M.08@ 106k, 25fps, video only, 40.57MiB
242          webm       320x240    240p  126k , webm_dash container, vp9@ 126k, 25fps, video only, 48.47MiB
396          mp4        480x360    360p  188k , mp4_dash container, av01.0.01M.08@ 188k, 25fps, video only, 72.01MiB
134          mp4        480x360    360p  221k , mp4_dash container, avc1.4d4015@ 221k, 25fps, video only, 84.73MiB
243          webm       480x360    360p  229k , webm_dash container, vp9@ 229k, 25fps, video only, 87.72MiB
397          mp4        640x480    480p  334k , mp4_dash container, av01.0.04M.08@ 334k, 25fps, video only, 127.98MiB
244          webm       640x480    480p  396k , webm_dash container, vp9@ 396k, 25fps, video only, 151.83MiB
135          mp4        640x480    480p  430k , mp4_dash container, avc1.4d401e@ 430k, 25fps, video only, 164.88MiB
18           mp4        480x360    360p  435k , avc1.42001E, 25fps, mp4a.40.2 (44100Hz), 166.58MiB (best)
```

Find the best format to fit the requirements above, in this example format code `133` will work best for video.

Download the video and audio (use `bestaudio` to automatically choose) and merge into an `mp4` container,

```bash
$ youtube-dl -f 133+bestaudio --merge-output-format mp4  https://www.youtube.com/watch?v=FZUfiW3W1KY
[youtube] FZUfiW3W1KY: Downloading webpage
[download] NEON PALM MALL (Vaporwave Mix + Video)-FZUfiW3W1KY.f133.mp4 has already been downloaded
[download] 100% of 35.73MiB
[download] Destination: NEON PALM MALL (Vaporwave Mix + Video)-FZUfiW3W1KY.f140.m4a
[download] 100% of 49.55MiB in 00:19
[ffmpeg] Merging formats into "NEON PALM MALL (Vaporwave Mix + Video)-FZUfiW3W1KY.mp4"
Deleting original file NEON PALM MALL (Vaporwave Mix + Video)-FZUfiW3W1KY.f133.mp4 (pass -k to keep)
Deleting original file NEON PALM MALL (Vaporwave Mix + Video)-FZUfiW3W1KY.f140.m4a (pass -k to keep)
```

## Playback

By default the console will blank after a period of time, turn that off so the screen is always on,

```bash
$ setterm -blank 0
```

Use `mplayer` to playback the video, the `fbdev2` device must be used, trying `directfb` for `fbdev` will result in an mplayer playback error.

```bash
$ mplayer -vo fbdev2 -fs -zoom NEON\ PALM\ MALL\ \(Vaporwave\ Mix\ +\ Video\)-FZUfiW3W1KY.mp4
```

If sound is too loud or quiet, ssh into the C.H.I.P. and use `alsamixer` to adjust the volume.

Keyboard controls for mplayer will work on the C.H.I.P. keyboard, with `q` to quit and arrow keys to browse the video.

## Notes

Overall resource usage isn't bad, about 25% CPU when playing the video back with just a slight audio glitch now and then. If CPU gets stressed, audio and playback will glitch even more. There are ways to tune mplayer to perform better on lower end systems like the C.H.I.P., but I won't go into detail here as there are many guides out there.

Depending on the video, the `mp4` output format may not work and give a `ERROR:   Stream #1:0 -> #0:1 (copy)` when trying to merge video+audio, using `mkv` for the output format is a workaround.
