---
layout: post
title: Enhancing my Macintosh 512Ke
category: macintosh
tags: macintosh 512k 512ke macplus system6 system7 retrocomputing
---

## Enhancing my Macintosh 512Ke

This is the second in a series of posts on my Macintosh 512Ke. In my [first post](/A-Macintosh-Story/) I went over the history of how I obtained this machine, initial exploration and repairs over the years.

[![Macintosh 512Ke Enhanced](/assets/images/posts/macintosh/macplus-enhanced.jpg){: width="60%"}](/assets/images/posts/macintosh/macplus-enhanced.jpg)
<figure><figcaption>My Macintosh 512Ke Enhanced in all its glory</figcaption></figure>

This post will go over the enhancements I've done to [my Macintosh 512Ke](https://en.wikipedia.org/wiki/Macintosh_512Ke#Official_upgrades) over the last six months. Getting it to the point where it can do useful, and modern day things, like writing blog posts in [MacWrite](https://en.wikipedia.org/wiki/MacWrite), surfing [Gopher](https://en.wikipedia.org/wiki/Gopher_(protocol)), [chatting on IRC](https://jcs.org/wallops) or [cruising a BBS](https://www.telnetbbsguide.com/bbs/captains-quarters-ii/) over WiFi and sharing files with modern Linux system. All of these enhancements are completely reversible and non-destructive if I ever want to to bring the machine back to its original stock state.

## FloppyEMU

A [FloppyEMU](https://www.bigmessowires.com/floppy-emu/) let's me use floppy images directly from an SD card, eliminating the need to use a floppy drive. The original 800k internal floppy drive suffered from [cheese-wheel-of-death](https://youtu.be/ia513LCN7jY) which I repaired, cleaned and lubricated for whenever I want to use real floppies, but I almost always prefer the FloppyEMU.

[![FloppyEMU](/assets/images/posts/macintosh/floppyemu-close.jpg){: width="60%"}](/assets/images/posts/macintosh/floppyemu-close.jpg)
<figure><figcaption>FloppyEMU displaying some disks</figcaption></figure>

## USB4VC

The [USB4VC](https://github.com/dekuNukem/USB4VC) allows me to use modern USB mice/keyboards on the machine, solving the problem I had of lacking the original M0110 keyboard. My usual keyboard of choice is a transparent blue [Monsgeek ICE75](https://www.monsgeek.com/product/ice75-fully-assembled/#) wireless keyboard and a clear blue wireless mouse because I feel it adds to the overall ａｅｓｔｈｅｔｉｃ.

[![usb4vc](/assets/images/posts/macintosh/usb4vc.jpg){: width="60%"}](/assets/images/posts/macintosh/usb4vc.jpg)
<figure><figcaption>USB4VC</figcaption></figure>

## Macintosh Plus Logic Board

I replaced the 512Ke logic board with a [Macintosh Plus](https://en.wikipedia.org/wiki/Macintosh_Plus) logic board providing 4MiB of memory (8x what the 512Ke has) and external SCSI port. This upgrade opens up many more use cases, such as running [MacTCP](https://en.wikipedia.org/wiki/MacTCP) which was impossible on a 512Ke.

Technically this also makes it no longer a 512Ke, and due to the port differences on the boards I had to replace the back case with Macintosh Plus case. Because of the case swap, the rear case is "Platinum" and the front "beige", giving it a slight two-tone look when viewed from the side. It also lacks the "Macintosh Plus" case badge on the front, making this machine a chimera of sorts. I also did a [SCSI term power mod](https://tinkerdifferent.com/resources/mac-plus-scsi-term-power-mod.123/) to the board to power the BlueSCSI without requiring an external power source.

[![MacPlus logic board](/assets/images/posts/macintosh/macplus-logicboard.jpg){: width="60%"}](/assets/images/posts/macintosh/macplus-logicboard.jpg)
<figure><figcaption>MacPlus logic board pre SCSI term mod</figcaption></figure>

## BlueSCSI

A [BlueSCSI](https://bluescsi.com/) hangs off the external SCSI port on the back of the MacPlus logic board, booting a System 7.0.1 image from its SD card. Because I splashed the extra $ and built it with a [RaspberryPi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html), it has the ability to emulate a [DynaPort](https://bluescsi.com/docs/WiFi-DaynaPORT) EtherTalk device and connect to The Internet using WiFi.

[![BlueSCSI](/assets/images/posts/macintosh/bluescsi.jpg){: width="60%"}](/assets/images/posts/macintosh/bluescsi.jpg)
<figure><figcaption>BlueSCSI</figcaption></figure>

## PicoRC

A [PicoRC](https://github.com/dekuNukem/PicoRC) provides power to the logic board and CRT portion of the analog board with a [PicoPSU](https://www.mini-box.com/picoPSU-80) ATX power supply and common AC power brick. It also allows easy access to the pinouts for Signal, H-Sync, V-Sync and GND pins from logic board wiring harness.

[![PicoRC](/assets/images/posts/macintosh/picorc.jpg){: width="60%"}](/assets/images/posts/macintosh/picorc.jpg)
<figure><figcaption>PicoRC connected to MacPlus logic board</figcaption></figure>

## Cooling

Original Classic Macintoshs were notorious for failing over time due to heat issues, and using the fan header on the PicoRC, I strapped a [Noctua NF-A4x10 Fan](https://www.amazon.com/dp/B00NEMGCIA) to the inside of the case with a zip tie. It doesn't move a ton of air and adds some noise to a previously silent machine, but it should help add a few more hours of life to the machine.

[![Fan inside case](/assets/images/posts/macintosh/fan.jpg){: width="60%"}](/assets/images/posts/macintosh/fan.jpg)
<figure><figcaption>Fan zip-tied to inside the case</figcaption></figure>

## RGB2HDMI

The [RGB2HDMI](https://github.com/hoglet67/RGBtoHDMI) can display the video output of the Macintosh over HDMI to any modern LCD monitor or video capture device. By soldering wires to the Signal, H-Sync, V-sync and Ground pinouts on the PicoRC I can tap into the video signal and can use both the internal CRT and an external display over the RGB2HDMI at the same time.

This is also my backup plan to continue using the machine if/when the CRT fails, as I can still use logic board and with the rest of these enhancements (USB4VC and PicoRO) to display to any monitor that supports HDMI.

[![RGB2HDMI](/assets/images/posts/macintosh/rgb2hdmi.jpg){: width="60%"}](/assets/images/posts/macintosh/rgb2hdmi.jpg)
<figure><figcaption>Displaying Finder on an both an external LCD and the internal CRT</figcaption></figure>

## TashTalk 2

The [TashTalk 2](https://ko-fi.com/s/60b561a0e3) is a RaspberryPi HAT that lets me connect my Macintosh using [PhoneNET](https://en.wikipedia.org/wiki/PhoneNET) adaptors to other devices with [AppleTalk](https://en.wikipedia.org/wiki/AppleTalk) networking. With this setup I can use [AppleShare](https://en.wikipedia.org/wiki/AppleShare) to share files and printers between other Macintoshes on the network. As an example I'm writing this post on the Macintosh Plus and saving it remotely over AppleShare, then copy it into this blog and publish it.

[![TashTalk2 HAT on a RaspberryPi 3](/assets/images/posts/macintosh/tashtalk2.jpg){: width="60%"}](/assets/images/posts/macintosh/tashtalk2.jpg)
<figure><figcaption>TashTalk2 HAT on RaspberryPi 3</figcaption></figure>

## Basilisk II

[Basilisk II](https://basilisk.cebix.net/) is not a modification, but a Macintosh 68k emulator for MacOS and Linux. I run System 7.5 Basilisk VM to download applications, extract files, and do things in a similar Macintosh environment but on faster hardware. The TashTalk2 RaspberryPi runs a [TashRouter](https://github.com/lampmerchant/tashrouter/) that and share files between Basilisk II and the Macintosh over AppleShare.

[![Basilisk II running on my Linux laptop](/assets/images/posts/macintosh/basilisk.jpg){: width="60%"}](/assets/images/posts/macintosh/basilisk.jpg)
<figure><figcaption>Basilisk II and video out from the Macintosh Plus</figcaption></figure>

## ROMinator

The most recent modification to my Macintosh is a [ROMinator](https://jcm-1.com/product/rominator-v1-for-macintosh-plus/) that replaces the original system ROM that shipped with the Plus. It provides all the features of the original ROM, but has extra features like changing the startup icon, startup sound and holding down R will boot into [System 6](https://en.wikipedia.org/wiki/System_6) from ROM.

[![ROMinator](/assets/images/posts/macintosh/rominator.jpg){: width="60%"}](/assets/images/posts/macintosh/rominator.jpg)
<figure><figcaption>ROMinator on the MacPlus logic board</figcaption></figure>

## Thoughts

Over the last six months I am surprised by how much I've learned about classic Macintoshs. I went from  booting 40 year old floppies, to connecting to Gopher sites and modern Linux systems and can use my Macintosh 512Ke (Plus) as I would a modern machine. The retro community around these systems is extremely impressive, creating tools and hardware that up until a few years ago didn't exist and I am grateful for the dedication and enthusiasm that others have for this platform.

There are still a few things I would like to do ([remote access...](https://jetkvm.com/)?) machine, but I am extremely happy with this setup and use it on a weekly basis, writing blog posts like this one, playing games, or just enjoying computing from when times were simpler and more optimistic.
