---
layout: post
title: Tailscale on the DevTerm R-01
description: Building a TUN/TAP Kernel Module to run Tailscale on a DevTerm R-01
category: devterm
tags: devterm riscv linux tailscale
toc: true
---

## Intro

Recently I assembled a [ClockworkPi DevTerm R-01](https://www.clockworkpi.com/product-page/devterm-kit-r01), a cyberdeck-like terminal with a [RISC-V](https://en.wikipedia.org/wiki/RISC-V) compute module. While the retro-future design of the DevTerm really appealed to me, and I've also been wanting to work with RISC-V for a while to learn a new architecture making the R-01 a perfect esoteric project platform.

![DevTermR01](/assets/images/posts/devtermtailscale/devterm-r01.png)
<figure><figcaption>ClockworkPi DevTerm R-01</figcaption></figure>

After trying out a few things like [DOSBox](https://www.dosbox.com/), [Surf](https://git.suckless.org/surf/), and [ScummVM](https://www.scummvm.org/), I found the [Allwinner D1](https://linux-sunxi.org/D1) RISC-V chip wasn't powerful enough to do much other than some basic window management, [Interactive Fiction](http://www.infocom-if.org/downloads/downloads.html), and browsing `gopher://` with [Bombadillo](https://bombadillo.colorfield.space/). However I still wanted to use it as a terminal to access other systems, which lead me to attempting to install [Tailscale](https://tailscale.com) to leverage the mesh VPN and other features.

Installing `tailscale` was un-eventful, as it's had [RISC-V support](https://github.com/tailscale/tailscale/issues/2119) for a while, and following the install guide did what was expected. The problem is `tailscaled` fails due to the required `tun` kernel module missing in the 5.4.61 kernel running on the DevTerm.

```
Jan 26 02:25:17 localhost systemd[1]: Started Tailscale node agent.
Jan 26 02:25:17 localhost tailscaled[1074605]: wgengine.NewUserspaceEngine(tun "tailscale0") ...
Jan 26 02:25:17 localhost tailscaled[1074605]: Linux kernel version: 5.4.61
Jan 26 02:25:17 localhost tailscaled[1074605]: is CONFIG_TUN enabled in your kernel? `modprobe tun` failed with: modprobe: FATAL: Module tun not found in directory /lib/modules/5.4.61
Jan 26 02:25:19 localhost tailscaled[1074605]: tun module not loaded nor found on disk
Jan 26 02:25:19 localhost tailscaled[1074605]: wgengine.NewUserspaceEngine(tun "tailscale0") error: tstun.New("tailscale0"): CreateTUN("tailscale0") failed; /dev/net/tun does not exist
Jan 26 02:25:19 localhost tailscaled[1074605]: flushing log.
Jan 26 02:25:19 localhost tailscaled[1074605]: logger closing down
```

## Building a TUN/TAP Kernel Module

The first step was finding if the R-01 kernel source was available so re-build the exact kernel version and include the `tun` module by setting `CONFIG_TUN=m`. Looking around the ClockworkPi website, Discord, and Github I eventually found the [How to Compile Kernel](https://github.com/clockworkpi/DevTerm/wiki/Create-DevTerm-R01-OS-image-from-scratch#how-to-compile-kernel) documentation. This had links to the original source and the toolchain.

Since the R-01 isn't exactly fast, cross-building this on a x86 system was required. My personal Debian server is a bit of mess when it comes to package pinning, so I created a new 8 CPU, 8GiB memory virtual machine in qemu and install [Ubuntu 22.04 "Jammy Jellyfish"](https://www.releases.ubuntu.com/jammy/) since that's what the R-01 is running and what ClockworkPi has in it's documentation.

### Installing Required Packages

After setting up the VM, install required packages for cross-building the kernel,

```sh
sudo apt-get install gcc-11-riscv64-linux-gnu binutils-riscv64-linux-gnu qemu-user-static build-essential git wget curl vim libncurses-dev flex automake autoconf bison libssl-dev
```

### Cloning ClockworkPi Kernel Source

Clone the [kernel source](https://github.com/cuu/last_linux-5.4) into `~/git`,

```sh
mkdir ~/git
git clone https://github.com/cuu/last_linux-5.4.git
```

### Setting Up Build Toolchain

Download the ClockworkPi toolchain from [https://github.com/cuu/toolchain-thead-glibc](https://github.com/cuu/toolchain-thead-glibc), which is a README pointing to a Mega link. While it's a bit concerning coming from Mega, since it's a tarball and running in a VM it's not that risky. There's also a section on installing the official RISC-V toolchain which is another option, but requires additional building.

Untar in home directory,


```sh
cd ~
tar -xvzf riscv64-glibc-gcc-thead_20200702.tar.gz
```

### Existing Kernel Config from DevTerm

Copy the running kernel config in `/proc/config.gz` on the DevTerm to the VM. The `config.gz` contains the configuration for how the running `5.4.61` kernel was configured and is loaded to set everything the exact same way when building the new kernel.

```sh
cd ~/git/last_linux-5.4
scp cpi@devterm:/proc/config.gz .
gunzip config.gz
mv config .config
```

### Enabling CONFIG_TUN

There are two ways to enable the TUN/TAP module,


- Edit `.config` and set `CONFIG_TUN=m`

or

- Interactively run `menuconfig` and set it in `Device Drivers -> Network device support -> Universal TUN/TAP device driver support `

```sh
export PATH=~/riscv64-glibc-gcc-thead_20200702/bin/:$PATH
make LOCALVERSION= CROSS_COMPILE=riscv64-unknown-linux-gnu- ARCH=riscv menuconfig
```
### Building the Kernel

Build the kernel using the provided `m.sh` script, but first edit it to include the `PATH` for the toolchain and `LOCALVERSION=`. If `LOCALVERSION=` isn't set then the kernel version will include a `+` at the end and modules will not load due to a version mis-match,

```sh
export PATH=~/riscv64-glibc-gcc-thead_20200702/bin/:$PATH
make LOCALVERSION= CROSS_COMPILE=riscv64-unknown-linux-gnu- ARCH=riscv
make LOCALVERSION= CROSS_COMPILE=riscv64-unknown-linux-gnu- ARCH=riscv INSTALL_MOD_PATH=test/rootfs/ modules_install
make LOCALVERSION= CROSS_COMPILE=riscv64-unknown-linux-gnu- ARCH=riscv INSTALL_PATH=test/boot/ zinstall
mkdir -p test/boot/
cp arch/riscv/boot/dts/sunxi/board.dtb test/boot/
```

Run `./m.sh` and wait a few minutes while it builds.

When successful, the new kernel and modules are in `test/boot/`

## Setting up New Modules on DevTerm

Create a tarball of the new modules and copy them to the DevTerm,

```sh
cd ~/git/last_linux-5.4/test/rootfs/lib/modules
tar -cvzf 5.4.61.modules.tar.gz 5.4.61/
scp 5.4.61.modules.tar.gz cpi@devterm:~
```

On the DevTerm, backup original modules directory,

```sh
cd /lib/modules
sudo mv 5.4.61 5.4.61.orig
```

and untar the new modules directory,

```sh
cd /lib/modules
sudo tar -xvzf ~/5.4.61.modules.tar.gz
```

### Loading the TUN/TAP Module

Load the new TUN/TAP Module,

```sh
sudo modprobe tun
```

If successfull `dmesg` will show,

```
tun: Universal TUN/TAP device driver, 1.6
```

### Setting up Tailscale

Now that the TUN/TAP module is loaded, start `tailscaled` and finish setting up Tailscale,

```sh
sudo service tailscaled start
sudo tailscale up
```
