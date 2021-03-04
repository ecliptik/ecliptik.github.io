---
layout: post
title: CHIP Serial Console
category: chip
tags: chip openbsd 100daystooffload hack raspberrypi

comments:
  show:  true
  fediHost:  fosstodon.org
  fediusername:  ecliptik
  fediid:  

---

Since [getting a Pocket C.H.I.P](https://www.ecliptik.com/Pocket-CHIP/), I'm looking for more ways to use it outside the original configuration, and came across a Hackernoon post on using a [CHIP as a serial console](https://medium.com/hackernoon/turn-your-pocketchip-into-a-badass-on-the-go-hardware-hackers-terminal-84b1edc939f).

I also wanted to [install OpenBSD onto a RaspberryPi 3](https://brainsnapped.com/2020/10/22/openbsd-on-the-raspberry-pi-3-model-b/) - unlike most RaspberryPi installs where a sdcard image is flashed and boots up - OpenBSD requires following the [full installation procedure](https://www.openbsd.org/faq/faq4.html) on the console. Sure you could hook up it up to HDMI and a USB keyboard, but what's the fun in that? So I took the oppurtunity to do both.

## Hardware

Following the Hackernoon post, and using the [RPI GPIO documentation](https://www.raspberrypi.org/documentation/usage/gpio/), I soldered some lead pins onto the CHIPs `5V`, `GND`, `TXD` and `RXD` breakout at the top, made some basic GPIO wires and hooked it all up. Using the `5V` has the added benefit of powering the RaspberryPi from the CHIP battery, which in makes both of them portable.

![C.H.I.P. Serial Console](/assets/images/posts/pocket-chip-serial.png)
<figure><figcaption>C.H.I.P. Serial Console</figcaption></figure>

## Software
To connect via serial console, first release `/dev/ttyS0` from systemd,

```bash
sudo systemctl stop serial-getty@ttyS0
```

Many articles suggest using [minicom](https://salsa.debian.org/minicom-team/minicom) as a serial console, but I prefer [screen](https://www.gnu.org/software/screen/), and used it for years when working in datacenters.

The OpenBSD console uses a baud rate of `115100` and transmission of eight bits per byte `cs8`. Connecting requires `sudo`, even if your `chip` user is in the `tty` group due to some udev/systemd permissions wonkiness.

```bash
sudo screen /dev/ttyS0 115200,cs8
```

<script id="asciicast-z1PtTyJIotvXQlLKK23MxjMh8" src="https://asciinema.org/a/z1PtTyJIotvXQlLKK23MxjMh8.js" async data-autoplay=1 data-loop=1 data-theme="tango" data-speed=".5"></script>
<figure><figcaption>Serial Console on RaspberryPi 3 Running OpenBSD</figcaption></figure>

The serial console works well, although occasionally there is missing data, but after remembering how to use the OpenBSD disk partitioner - OpenBSD 6.8 was running on a RaspberryPi 3. Once the installation is complete, if DHCP was setup during install, connecting to it over ssh is trivial and no longer requires the serial console.

## Conclusion

While as much fun as this is, it's not nearly as useful as it could have been years ago when troubleshooting misbehaving [Sun Netra](https://shrubbery.net/~heas/sun-feh-2_1/Systems/Netra_t1_105/spec.html) or [Sun Fire](https://shrubbery.net/~heas/sun-feh-2_1/Systems/SunFire280R/SunFire280R.html) systems. For now though it's a good hack, useful in the right circumstances, and just looks cool.
