---
layout: post
title: Live, Laugh, Localtalk with Basilisk II
category: macintosh
tags: basilisk localtalk appletalk macintosh 512k 512ke macplus system6 system7 retrocomputing
---

As I mentioned in my post on [Enhancing my Macintosh 512Ke](/Enhancing-my-Macintosh-512Ke/) I use the [Basilisk II](https://basilisk.cebix.net/) Macintosh 68k emulator alongside my Macintosh Plus to facilite downloading software, copying files, using AppleShare and other things. It works really well as a bridge between my classic Macintosh and modern systems, especially when it comes to transferring files between the two using [AppleShare](https://en.wikipedia.org/wiki/AppleShare).

Below is a short guide on how I installed it and setup Basilisk II to work with this older system.

## Installing Basilisk II

Basilisk II is available in the main Ubuntu, Linux Mint and Debian repos and other Linux distros probably have it too

To install it with `apt` on a Debian based distro,

```sh
sudo apt update
sudo apt install -y basilisk2
```

## Setting Up Basilisk

Basilisk requires a few things to setup, most notable a sytem ROM and disk image. It also can mount a shared folder with the host filesystem to make copying files in/out of the VM relatively easy.

Start by creating directories for ROMs, disks and file sharing

```sh
mkdir -p ~/Documents/basilisk
cd ~/Documents/
mkdir roms unix disks
```

Find and copy a ROM file into `~/Documents/basilisk/roms`, for my setup I use `PERFORMA.ROM` ROM.

In the `Memory/Misc` tab, configure the machine with the following,

- MacOS RAM Size (MB): 128 (or higher)
- Mac Model ID: Mac IIci (MacOS 7.X)
- CPU Type: 68040
- ROM File: `~/Documents/basilisk/roms/PERFORMA.ROM`

[![Basilisk II Memory/Misc Tab](/assets/images/posts/macintosh/basilisk-settings.png)](/assets/images/posts/macintosh/basilisk-settings.png)
<figure><figcaption>Basilisk II Memory/Misc Tab</figcaption></figure>

A full Install of System 7.5.5 is required in order to use AppleShare and most applications. Disk images are available various places online or you can follow [a guide](https://www.savagetaylor.com/2018/09/02/setting-up-your-vintage-classic-68k-macintosh-installing-the-full-version-of-system-7-5-5-or-6-0-8/) to make your own, which is what I did.

## Using Basilisk

With the system configuration completed and a 7.5.5 disk image, turn on the VM by clicking the Start button and default desktop will appear with a few icons like the disk drive and trash.

[![Default 7.5.5 Desktop in Basilisk](/assets/images/posts/macintosh/basilisk-755-desktop.png)](/assets/images/posts/macintosh/basilisk-755-desktop.png)
<figure><figcaption>Default 7.5.5 Desktop in Basilisk</figcaption></figure>

## AppleTalk over TCP/IP

Getting LocalTalk and AppleTalk to work on a 7.5.5 in Basilisk and communicate with other Macintosh devices using the hosts wireless networking requires the `sheep_net` kernel module.

The module is available in the [macemu](https://github.com/cebix/macemu) repository and requires building it for your system and kernel version. This also means that everytime there is a kernel upgrade, you will need to re-build the module.

To build the kernel module,

```sh
git clone https://github.com/cebix/macemu.git
cd macemu/BasiliskII/src/Unix/Linux/NetDriver
make
sudo make install
```

Load the `sheep_net` kernel module and update it's permissions so users other than root can use it. This must also be done on every reobot and I should probable script this out and put it somewhere like `rc.local`.

```sh
sudo modprobe sheep_net
sudo chmod 777 /dev/sheep_net
```

Finally, in the Serial/Network tab of Basilisk, change the Ethernet Interface to your wireless or Ethernet device that's connected to your LAN.

[![Basilisk Network Tab](/assets/images/posts/macintosh/basilisk-networking.png)](/assets/images/posts/macintosh/basilisk-networking.png)
<figure><figcaption>Basilisk Network Tab</figcaption></figure>

After starting the VM will see other devices using AppleTalk on your local network, and if you have a [TashTalk](https://github.com/lampmerchant/tashtalk) and [TashRouter](https://github.com/lampmerchant/tashrouter/), older LocalTalk devices like a [Macintosh Plus](/Enhancing-my-Macintosh-512Ke/) are also available.

Now you can share files and printers between devices with AppleTalk over a modern network.

[![AppleShare in Basilisk](/assets/images/posts/macintosh/basilisk-appleshare.png)](/assets/images/posts/macintosh/basilisk-appleshare.png)
<figure><figcaption>AppleShare in Basilisk</figcaption></figure>
