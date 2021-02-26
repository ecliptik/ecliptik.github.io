---
layout: post
title: Pocket C.H.I.P.
category: hack
tags: debian chip hack 100daystooffload

comments:
  show:  true
  fediHost:  fosstodon.org
  fediusername:  ecliptik
  fediid:  105789701988446339

---

Recently I got a [Pocket C.H.I.P.](https://shop.pocketchip.co/) with the idea of making it mini terminal on my desk, displaying things like weather, new email, new mastodon toots, etc. It comes pre-loaded with some basic software: terminal, [pico8](https://www.lexaloffle.com/pico-8.php), and a few other utilities. Because it was released in 2017 and the demise of the original Next Thing the software on it is out-of-date, running Debian 8 and an older version of pico8.

![Pocket C.H.I.P.](/assets/images/posts/pocket-chip.png)
<figure><figcaption>Pocket C.H.I.P.</figcaption></figure>

I wanted to updated it to at least Debian 10, and found a [working guide](https://gist.github.com/luzhuomi/526fbcc30f3522f09eacf20d0f776fa5) which follows the basic Debian upgrade process as well as some fixes for common issues like Xorg configs and updating wifi settings.

Unfortunately this broke a few other things that weren't listed in the guide, like the FN keys no longer working on the built-in keyboard and pico8 failing to start. I spent some time tackling these issues and now have a fully working Debian 10 Pocket C.H.I.P. with pico8 and a functioning keyboard.

## Fixing FN Keys

After upgrading to Debian 10, the `FN` keys on the C.H.I.P. build-in keyboard will no longer work. Fix this by sourcing the keymap in `/home/chip/.xinitrc` and restarting C.H.I.P. for xorg to load the xmodmap every time.

```bash
[[ -f /home/chip/.Xmodmap ]] && xmodmap /home/chip/.Xmodmap
```

For reference `/home/chip/.Xmodmap` is,

```
keycode 10 = 1 exclam F1 exclam
keycode 11 = 2 at F2 at
keycode 12 = 3 numbersign F3 numbersign
keycode 13 = 4 dollar F4 dollar
keycode 14 = 5 percent F5 percent
keycode 15 = 6 asciicircum F6 asciicircum
keycode 16 = 7 ampersand F7 ampersand
keycode 17 = 8 asterisk F8 asterisk
keycode 18 = 9 parenleft F9 parenleft
keycode 19 = 0 parenright F10 parenright
keycode 22 = BackSpace BackSpace KP_Delete BackSpace
keycode 29 = y Y braceleft Y
keycode 30 = u U braceright U
keycode 31 = i I bracketleft I
keycode 32 = o O bracketright O
keycode 33 = p P bar P
keycode 36 = Return NoSymbol KP_Enter
keycode 43 = h H less H
keycode 44 = j J greater J
keycode 45 = k K apostrophe K
keycode 46 = l L quotedbl L
keycode 56 = b B grave b
keycode 57 = n N asciitilde n
keycode 58 = m M colon M
keycode 59 = comma less semicolon less
keycode 60 = period comma semicolon comma
keycode 61 = slash question backslash question
keycode 82 = KP_Subtract underscore F11 KP_Subtract
keycode 86 = KP_Add KP_Equal F12 KP_Add
keycode 108 = Mode_switch Meta_R Alt_R Meta_R
keycode 111 = Up NoSymbol Prior
keycode 113 = Left NoSymbol Home
keycode 114 = Right NoSymbol End
keycode 116 = Down NoSymbol Next
```

## Updating Pico8

Downloaded latest Pico8 for the C.H.I.P. from [lexaloffle.com](https://www.lexaloffle.com/bbs/?tid=34009) and follow the instructions on installing it.

The binary was built against an old version of `libcurl` and will give error about not finding `CURL_OPENSSL_3`.

```bash
./pico8: /usr/lib/arm-linux-gnueabihf/libcurl.so.4: version `CURL_OPENSSL_3' not found (required by ./pico8)
```

To fix this, download the older [Raspian Stretch image](https://downloads.raspberrypi.org/raspbian/images/raspbian-2017-09-08/) and mount it locally

```bash
sudo mount -v -o offset=48234496 -t ext4 2017-09-07-raspbian-stretch.img /mnt
```

Create the directory `/usr/local/share/libcurlhack` and copy the files `/mnt/usr/lib/arm-linux-gnueabihf/{libcrypto.so.1.0.2,libcurl.so.4,libssl.so.1.0.2}` from the Raspbian Stretch image to the C.H.I.P.

When finished the C.H.I.P. `/usr/local/share/libcurlhack/` will look like this,
```bash
chip@chip:~$ ls -l /usr/local/share/libcurlhack/
total 2208
-rw-r--r-- 1 root staff 1493272 Feb 24 02:20 libcrypto.so.1.0.2
-rw-r--r-- 1 root staff  439956 Feb 24 02:15 libcurl.so.4
-rw-r--r-- 1 root staff  320924 Feb 24 02:19 libssl.so.1.0.2
```

Create a shell script `/usr/local/bin/pico8` that will include this new path in `LD_LIBRARY_PATH`,

```bash
#!/bin/sh

LD_LIBRARY_PATH=/usr/local/share/libcurlhack:/usr/lib/arm-linux-gnueabihf/
export LD_LIBRARY_PATH

/usr/lib/pico8/pico8
```

Running Pico8 from the Pocket C.H.I.P. launcher will now work.

## Changing the Window Manager

By default the C.H.I.P. will run the `pocket-wm`, which is a modified version of [dwm](https://dwm.suckless.org/).

```bash
chip@chip:/usr/share/xsessions$ pocket-wm -v
dwm-6.0, © 2006-2011 dwm engineers, see LICENSE for details
```

This in turn runs [dmenu](https://tools.suckless.org/dmenu/) and to launch the "home" screen with the applications Iceweasel, pico8, urxvt, and aeabi.

```
chip@chip:~$ strings /usr/bin/pocket-wm | grep dmenu_run -A4
dmenu_run
Iceweasel
pico8
urxvt
aeabi
```

I looked a bit to see how all this was configured, but need to spent more time on reading up on `dwm` and `dmenu_run` to know what I'm looking at.

To run a different window manager or session we'll need to configure [Lightdm](https://github.com/canonical/lightdm) to use something other than `pocket-wm`.

For example to run [Fluxbox](http://fluxbox.org/), install it using `apt`,

```bash
sudo apt-get update && sudo apt-get install -y fluxbox
```

Which creates `fluxbox.desktop` in `/usr/share/xsessions`. This directory contains all available window managers that Lightdm can launch.

```bash
chip@chip:~$ ls -l /usr/share/xsessions
total 24
-rw-r--r-- 1 root root  188 Feb 26  2019 awesome.desktop
-rw-r--r-- 1 root root  222 Feb 24  2014 fluxbox.desktop
-rw-r--r-- 1 root root   86 Feb 22  2019 lightdm-xsession.desktop
-rw-r--r-- 1 root root  118 Apr 27  2016 pocket-wm.desktop
-rw-r--r-- 1 root root 5465 Oct 21  2017 xfce.desktop
```

In the `chip` users home directory `~/.dmrc` and set `Session=` to the window manager lightdm should launch automatically. This will match what's in `/usr/share/xessions` but without the `.desktop` extension This will match what's in `/usr/share/xessions` but without the `.desktop` extension.

```
[Desktop]
Language=en_US.utf8
Session=fluxbox
```

Restart `lightdm` and it will restart the C.H.I.P. with the new window manager.

```
sudo systemctl restart lightdm
```

![Fluxbox on PocketCHIP](/assets/images/posts/fluxbox-chip.png)
<figure><figcaption>Fluxbox on PocketChip</figcaption></figure>


### Right Click
Right click is heavily used on Fluxbox but doesn't work out-of-the-box with the Pocket C.H.I.P., and setting a button override in Xmodmap or mouse keys in Xorg doesn't work (it even seems to break the FN keys). To enable right click by holding down on the touch screen build and setup [evdev-right-click-emulation](https://github.com/PeterCxy/evdev-right-click-emulation).

```bash
# Clone the repoistory
git clone https://github.com/PeterCxy/evdev-right-click-emulation

# Install required dependencies to build
sudo apt-get install -y libevdev-dev libevdev2

# Build evdev-rce
make all

# Move evdev-rce to a system path and chown the owner group
sudo mv out/evdev-rce /usr/local/bin
sudo chown root:staff /usr/local/bin/evdev-rce

# Have evdev-rce start on boot
echo "/usr/local/bin/evdev-rce &" | sudo tee -a /etc/rc.local
```

## Conclusion

the Pocket C.H.I.P. is a lot of fun, even with some of these issues the troubleshooting process gave me a way to explore the system and understand how it works. This is valuable as I continue to tinker with it to make it a true desk mini-terminal.
