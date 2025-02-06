---
layout: post
title: Enhancing my Macintosh 512Ke
category: macintosh
tags: macintosh 512k 512ke macplus system6 system7 retrocomputing
---

## Enhancing my  Macintosh 512Ke

This is the second in a series of posts on my Macintosh 512Ke. In the [first post](/A-Macintosh-Story/) I went over the history of how I obtained it some intial exploration, repairs and using it without a keyboard.

In this post I'll go over the enhancements I've done to my already [enhanced Macintosh 512Ke](https://en.wikipedia.org/wiki/Macintosh_512Ke#Official_upgrades). Getting it to the point where it can do useful to do modern day things like writing blog posts, browsing [Gopher](https://en.wikipedia.org/wiki/Gopher_(protocol)), [chatting on IRC](https://jcs.org/wallops) or [cruising a BBS](https://www.telnetbbsguide.com/bbs/captains-quarters-ii/). All of these enhancements are completely reversable and non-destructive if I ever want to it back to stock again as well.

## FloppyEMU

The [FloppyEMU](https://www.bigmessowires.com/floppy-emu/) let's me use floppy images directly from an SD card, eliminating the need to use a floppy drive entirely. The original 800k drive suffered from "cheese-wheel-of-death" and I repaired it, so it can use real floppies if needed too.

[![My Macintosh](/assets/images/posts/macintosh/floppyemu.jpg){: width="60%"}](/assets/images/posts/macintosh/floppyemu.jpg)
<figure><figcaption>FloppyEMU</figcaption></figure>

## USB4VC

The [USB4VC](https://github.com/dekuNukem/USB4VC) allows me to use modern USB mice/keyboards on the machine, solving the problem I had of no original keyboard. I usually use a blue [Monsgeek ICE75](https://www.monsgeek.com/product/ice75-fully-assembled/#) wireless keyboard and a clear blue wireless mouse because I feel it adds to the overall ａｅｓｔｈｅｔｉｃ.

[![usb4vc](/assets/images/posts/macintosh/usb4vc.jpg){: width="60%"}](/assets/images/posts/macintosh/usb4vc.jpg)
<figure><figcaption>USB4VC</figcaption></figure>

## Macintosh Plus Logic Board

I replaced the 512Ke logic board with a [Macintosh Plus](https://en.wikipedia.org/wiki/Macintosh_Plus) board with 4MiB of memory (8x what the 512Ke has) and external SCSI port. Technically this no longer makes it a 512Ke, but due to the port differences on the boards I replaced the back case seciton with Macintosh Plus case. This makes the rear of the machine "Platnium" and the front "beige", giving it a slight two-tone look. It also lacks the "Macintosh Plus" case badge, making this machine a chimera of sorts.

[![MacPlus logic board](/assets/images/posts/macintosh/macplus-logicboard.jpg){: width="60%"}](/assets/images/posts/macintosh/macplus-logicboard.jpg)
<figure><figcaption>MacPlus logic board</figcaption></figure>

## BlueSCSI

A [BlueSCSI](https://bluescsi.com/) hangs off the external SCSI port on the MacPlus logic board, booting a System 7.0.1 image from its SD card. Because I spent the extra $, and built it with a [RaspberryPi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html) it can emulate a [DynaPort](https://bluescsi.com/docs/WiFi-DaynaPORT) EtherTalk device and connect to The Internet using wifi.

[![BlueSCSI](/assets/images/posts/macintosh/bluescsi.jpg){: width="60%"}](/assets/images/posts/macintosh/bluescsi.jpg)
<figure><figcaption>BlueSCSI</figcaption></figure>

## PicoRC

A [PicoRC](https://github.com/dekuNukem/PicoRC) provides power to the logic board and to the CRT portion of the analog board with a [PicoPSU](https://www.mini-box.com/picoPSU-80) and modern power brick. It also has easy access to the pinouts for Signal, H-Sync, V-Sync and GND pins from logic board wiring harness.

[![PicoRC](/assets/images/posts/macintosh/picorc.jpg){: width="60%"}](/assets/images/posts/macintosh/picorc.jpg)
<figure><figcaption>PicoRC connected to MacPlus logic board</figcaption></figure>

## Cooling Fan

Original Classic Macintoshs were notorious for failing over time due to heat and low airflow, so using the fan header on the PicoRC, I strapped a [Noctua NF-A4x10 Fan](https://www.amazon.com/dp/B00NEMGCIA?ref=ppx_yo2ov_dt_b_fed_asin_title) to the insde of the case with a zip tie. It's not super powerful, and it adds some noise to a previously silent machine, but it should help add a few more house of life to the machine.

[![Fan inside case](/assets/images/posts/macintosh/fan.jpg){: width="60%"}](/assets/images/posts/macintosh/fan.jpg)
<figure><figcaption>Fan zip-tied to inside the case</figcaption></figure>

## RGB2HDMI

The [RGB2HDMI](https://github.com/hoglet67/RGBtoHDMI) can display the video output of the Macintosh over HDMI to any modern LCD monitor or video capture device. Soldering wires to the the Signal, H-Sync, V-sync and Groud pinouts on the PicoRC I can tap into the video signal and can use both the internal CRT and an external display over the RGB2HDMI at the same time. This is also my backup plan to continue using the machine if/when the CRT fails, as I can pull out the logic board and with the rest of these enhancements us it on any monitor that supports HDMI.

[![RGB2HDMI](/assets/images/posts/macintosh/rgb2hdmi.jpg){: width="60%"}](/assets/images/posts/macintosh/rgb2hdmi.jpg)
<figure><figcaption>Displaying Finder on an external LCD and the internal CRT</figcaption></figure>

## TashTalk 2

The [TashTalk 2](https://ko-fi.com/s/60b561a0e3) is a RaspberryPi HAT that lets me connect my Macintosh using [PhoneNET](https://en.wikipedia.org/wiki/PhoneNET) adaptors to other devices with [AppleTalk](https://en.wikipedia.org/wiki/AppleTalk) networking. With this setup I can use [AppleShare]() to share files and printers between other Macintoshes on the network. As an example I'm writing this post on the Macintosh Plus and saving it remotely over AppleShare, then copy it into this blog and publish it.

[![TashTalk2 HAT on a RaspberryPi 3](/assets/images/posts/macintosh/tashtalk2.jpg){: width="60%"}](/assets/images/posts/macintosh/tashtalk2.jpg)
<figure><figcaption>TashTalk2 HAT on RaspberryPi 3</figcaption></figure>

## Basilik II

[Basilisk II](https://basilisk.cebix.net/) is not a modification, but a Macintosh 68k emulator for MacOS and Linux. I run System 7.5 Basilisk VM to download applications, extract files, and do things in a similar Macintosh environment but on faster hardware. The TashTalk 2 RaspberryPi runs a [TashRouter](https://github.com/lampmerchant/tashrouter/) that connects Basilik II my Macintosh Plus over AppleTalk.

[![Basilik II running on my Linux laptop](/assets/images/posts/macintosh/basilisk.jpg){: width="60%"}](/assets/images/posts/macintosh/basilisk.jpg)
<figure><figcaption>My Macintosh editing this blog post in MacWrite</figcaption></figure>

## Rominator

The most recent modifiation to my Macintosh is a [ROMinator](https://jcm-1.com/product/rominator-v1-for-macintosh-plus/) that replaces the original system ROM that shipped with the Plus. It provides all the features of the original ROM, but has extra features like changing the startup icon and sound and booting into System 6 directly from the ROM.
[![ROMinator](/assets/images/posts/macintosh/rominator.jpg){: width="60%"}](/assets/images/posts/macintosh/rominator.jpg)
<figure><figcaption>ROMinator on the MacPlus logicboard</figcaption></figure>
