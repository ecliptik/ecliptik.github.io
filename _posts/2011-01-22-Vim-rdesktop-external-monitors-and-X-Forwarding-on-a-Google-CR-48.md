---
layout: post
title: Vim, rdesktop, external monitors, and X Forwarding on a Google CR-4
category: blogger
tags: vim google cr-48 linux blogger
---
While there are my other impressive hacks going around for the CR-48, [minecraft](https://www.minecraftforum.net/forums/minecraft-java-edition/discussion/120216-minecraft-on-the-cr-48-google-chrome-laptop), [ubuntu](https://sites.google.com/a/chromium.org/dev/chromium-os/developer-information-for-chrome-os-devices/cr-48-chrome-notebook-developer-information/how-to-boot-ubuntu-on-a-cr-48), I needed a few utilities that were more pragmatic. The following assumes that your CR-48 is in [developer mode](https://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices/cr-48-chrome-notebook-developer-information) and you have a basic understanding of bash, scp, and compiling source code under GNU/Linux.

# Vim

When I first went into the developer shell I saw approximately 1000 different binaries to run, but not one of them was a text editor. Eventually I stumbled upon qemacs, but we're just on a CR-48 not the middle ages. It was time to figure out how to get vim up and running.

Although ChromeOS is it's own GNU/Linux distro, it appears to mimic Debian/Ubuntu and is adhering somewhat to the LSB. I first just tried a straight copy of the vim binary from a Ubuntu 10.04 system but after some investigating with ldd saw it had a lot of shared libraries that weren't available on the CR-48 (most notably libselinux.so). So the quickest way to get around this was to build a static binary on a 32-bit Debian host (Ubuntu works as well).

On a 32-bit Debian Squeeze I downloaded latest [VIM source code](https://www.vim.org/sources.php) and built a static binary with a limited set of features and disabling GUI and selinux options:

```console
USER@DEBIAN ~ $ wget ftp://ftp.vim.org/pub/vim/unix/vim-7.3.tar.bz2
USER@DEBIAN ~ $ tar -xvjf vim-7.3.tar.bz2
USER@DEBIAN ~ $ cd vim73
USER@DEBIAN ~ $ export LDFLAGS=-static
USER@DEBIAN ~ $ ./configure --with-features=small --disable-gui --with-vim-name=vi --disable-selinux
USER@DEBIAN ~ $ make
```

This will make a static binary called `vi' in the `src' directory. On the CR-48 in `/home/chronos/user' make a directory called `bin' and scp the `vi' binary to it.

Try and execute it, but you'll get a *Permission Denied* error because by default the `/home/chronos/user' directory is mounted with the `noexec' option. Fix this by remounting it with `exec.'

```console
    chronos@localhost ~ $ sudo mount -i -o remount,exec /home/chronos/user
```

Now the binary will run and you have a basic vi editor.

# rdesktop


Rdesktop is much easier to put on the CR-48 since all of the libraries are available. From a 32-bit Debian/Ubuntu host, or by downloading the [rdesktop i686 package](https://packages.debian.org/rdesktop) from packages.debian.org, copy the rdesktop binary to the `/home/chronos/user/bin' directory. If it's mounted with `exec' then it will just run. Pass it whatever options you like, and it will open a new GUI window on the CR-48, completely independent of the Chrome UI and any shells.

```console
chronos@localhost ~ $ ~/bin/rdesktop -u USERNAME -g 1280x800 -K -z -r clipboard:PRIMARYCLIPBOARD HOSTNAME
```

Copy/paste works well, although the arrow keys may not function properly due to the keymap not getting set correctly. This may be due to a libiconv issue and I'll need to spend some more time figuring it out.

# External Monitors

While the CR-48 works just fine with it's VGA output without much tweaking, you'll either need to sign in/out or reboot the laptop for it to display to an external monitor. In dev mode xrandr is available making it easy to switch between display resolutions.


Mirror to a monitor that can do 1024x768:

```console
chronos@localhost ~ $ ~/bin/rdesktop -u USERNAME -g 1280x800 -K -z -r clipboard:PRIMARYCLIPBOARD HOSTNAME
chronos@localhost ~ $ xrandr --output LVDS1 --mode 1024x768 --output VGA1 --mode 1024x768
```

Turn off the external display and reset the CR-48 display back to the default 1280x800:

```console
chronos@localhost ~ $ xrandr --output LVDS1 --mode 1280x800 --output VGA1 --off
```

# X Forwarding

The simplest piece to enable is X-forwarding from a remote X client. Connect over ssh with the `-Y` option and run any X applications:

```console
chronos@localhost ~ $ ssh -Y USER@HOSTNAME
```
# Bringing It All Together

Now that all the binaries are in place let's set it up so they work across reboots.

Edit `/home/chronos/user/.bashrc' with our new vi editor and append the following:

```shell
#Setup our environment
source ~/.bash_aliases
PATH=$PATH:~/bin

#Remount /home/chronos/user as exec so anything in ~/bin runs
sudo mount -i -o remount,exec /home/chronos/user
```

Create a `/home/chronos/user/.bash_aliases` and add in any aliases:

```shell
alias rdesktop-home='~/bin/rdesktop -g 1280x800 -u USER -K -z -r clipboard=PRIMARYCLIPBOARD HOSTNAME'
alias projon='xrandr --output LVDS1 --mode 1024x768 --output VGA1 --mode 1024x768'
alias projoff='xrandr --output LVDS1 --mode 1280x800 --output VGA1 --off'
alias ssh-host='ssh -Y USER@HOSTNAME'
```

Now you have a much more flexible environment to add your own aliases, functions, and binaries.

