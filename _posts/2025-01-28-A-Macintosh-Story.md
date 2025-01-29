---
layout: post
title: A Macintosh Story
category: macintosh
tags: macintosh 512ke 512k macplus system6 system7 retrocomputing
---

# A Macintosh History

This is the first post in what I am hoping to be a series of how I took a [512ke "Fat Mac"](https://en.wikipedia.org/wiki/Macintosh_512Ke) and modified it to make it My Macintosh.

[![My Macintosh](/assets/images/posts/macintosh/my-macintosh.jpg){: width="60%"}](/assets/images/posts/macintosh/my-macintosh.jpg)
<figure><figcaption>My Macintosh editing this blog post in MacWrite</figcaption></figure>

## Releasing the Magic Smoke

Our story begins a dozen years ago when I inherited the 512ke Mac from a nursery school. I had at one point turned it on to check if it worked and test out a few of the floppies it came with, but it wasn't until years later when I thought our kids would like to see it in action in during COVID that I did anything else with it. With them watching, I booted it up with [Dinosaur Discovery Kit](https://www.mobygames.com/game/200750/dinosaur-discovery-kit/) for them to play, which they enjoyed, but 5 minutes later there was a loud pop and a lot of smoke coming out of the case. After quickly moving the kids to a safe distance and bringing it outside, I realized it was still functioning normally even with all that smoke until I had powered hit off.

Researching into what happened, I learned that older macs, like many systems from the 1980s used RIFA capacitors that were [notorious for failing in a spectacular manner](https://www.eevblog.com/forum/chat/old-rifa-capacitors-and-a-disaster-story/). Researching more I found that you could get a relatively inexpensive modern day replacement. I also decided to recap the entire "analog" board, as the capacitors over time could leak and cause all sorts of issues.

[![RIFA](/assets/images/posts/macintosh/rifa.jpg){: width="60%"}](/assets/images/posts/macintosh/rifa.jpg)
<figure><figcaption>Blown RIFA capacitor</figcaption></figure>

A few online purchases and days later I had replacement capacitors and slowly went through desoldering the old ones and soldering the new ones onto the analog board. Learning about proper CRT discharge procedures as the analog board could provide quite a shock due to the high voltage running through it. Once replaced the 512k worked just fine, and Dinosaur Discovery Kit and other software booted off the floppy without issue.

I used the machine a bit more, but found it limited in what it could do, especially with many of the floppies I had not working at all. I shelved the system again, satisfied it "worked" but didn't have much use for it other than looking nice on a shelf in the garage behind me during Zoom meetings..

## FloppyEMU

Sometime in 2024 while watching retro computer youtube videos I saw a someone use a [FloppyEMU](https://www.bigmessowires.com/floppy-emu/) to emulate an external floppy drive and run Macintosh programs downloaded from websites like [Macintosh Garden](https://macintoshgarden.org/) and [Macintosh Repository](https://www.macintoshrepository.org/) directly off an SD card. It could even emulate a [Hard Disk 20 ](https://en.wikipedia.org/wiki/Hard_Disk_20) with a 20MiB storage capacity.

Reading more about the FloppyEMU opened up many possibilities, no more would I be limited to the floppy disks I had, but could run practically any Macintosh software that the 512k would run, just find it, copy to an SD card and boot. The possibilities were endless.

I ordered one and after a few days it arrived, it was relatively easy to assemble and soon I was able to boot off of it, trying out all sorts of software and it completely changed how I could use the machine. It also greatly increased my knowledge of how early Macintoshes worked. Most of my computing experience has involved operating systems installed to permanent storage, like a hard drive, booting off of it and then running programs. Where with the Macintosh there was an Operating System, but you mostly booted into programs directly, they still had a Finder but were very limited and you would have to switch disks if you wanted to do something else.

[![FloppyEMU running Dark Castle](/assets/images/posts/macintosh/floppyemu.jpg){: width="60%"}](/assets/images/posts/macintosh/floppyemu.jpg)
<figure><figcaption>FloppyEMU running Dark Castle</figcaption></figure>

While the FloppyEMU made this easier, it was starting to show some of it's own flaws, such as "File not contiguous" errors. After a lot of reading, I found that copying files from my modern Macbook via Finder to the SD card wouldn't write them in a single stream of data, confusing the FloppyEMU. Copying disk images from my Linux system worked better, but depending on the file format, download site and many other options this was a continuous challenge.

## HD20

My frustrations with booting the FloppyEMU as a floppy drive lead to using it's feature of [emulating a Hard Disk 20](https://www.savagetaylor.com/2020/03/29/booting-a-macintosh-plus-with-floppyemus-hd20-support/). This resolved the problems I was having with continually removing the SD card, copying the disk images to it, booting up the 512k and then hoping it would work. Now I could copy almost as many disk images as I wanted to the HD20 and have it boot into the System 6 operating system directly, using it more or less like a modern computer.

While using this technique, I ended up keeping notes of what all software worked and what didn't with the error messages on those that didn't. One that kept repeating itself was the 512k simply running out of memory. In my solution of booting to System 6 on the HD20, I inadvertently used up much of the precious 512k of memory for the OS, further limiting what software I could run unless I booted directly too it from the FloppyEMU, bringing me back to square one.

## No Keyboard Detected

As an aside, while doing all of this, I was still missing one major component - a keyboard. Because the original Macintosh was so focused on using a mouse, I was able to do all of the above with the original [M0100 mouse](https://en.wikipedia.org/wiki/Apple_pointing_devices#Macintosh_Mouse_(M0100)) it came with, but I didn't have a [M0110 keyboard](https://en.wikipedia.org/wiki/Apple_keyboards#Macintosh_Keyboard_(M0110)) to use with the system. There were some on Ebay, but they were almost, if not more, expensive than the 512k itself and I would need to start looking for alternative options.

## Input/Output

Up until this point I as really enjoying using the 512ke, and the software I could run with only the mouse was a lot of fun to use, but I wanted more. Seeing some videos about the SE/30 and watching the [series of videos JCS had done on their 512k](https://jcs.org/system6c) programming new System 6 software on the system itself, I wanted to do more.

I knew there was a big enough [vintage Macintosh community](https://68kmla.org/bb/index.php) to support something like the FloppyEMU, so that must mean there are other projects out there right? What else could I do with the system to push it even further, avoiding memory issues, suing a modern keyboard, and maybe even getting it online? That rabbit hole was much deeper than I was expecting.
