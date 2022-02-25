---
layout: post
title: Gemini Capsule in a FreeBSD Jail
category: hack
tags: freebsd hack gemini 100daystooffload
toc: true

comments:
  show:  true
  fediHost:  fosstodon.org
  fediusername:  ecliptik
  fediid:  106130559129256903

---

With the [recent release of FreeBSD 13](https://www.freebsd.org/releases/13.0R/announce/), I wanted to test it out on a spare RaspberryPi 3 that was part of my [old Kubernetes cluster](https://www.ecliptik.com/Raspberry-Pi-Kubernetes-Cluster/).

In particular, [FreeBSD Jails](https://docs.freebsd.org/en/books/handbook/jails/) have always interested me, although I've never used them in practice. Over the years I've managed [operating system virtualization](https://en.wikipedia.org/wiki/OS-level_virtualization) through Solaris Zones and Docker containers, and Jails seem like and good middle ground between the two - easier to manage than zones and closer to the OS than Docker.

I also want to run my own [Gemini](https://gemini.circumlunar.space) capsule locally to use some of the features that my other hosted capsules don't have (like SCGI/CGI) and setting up a capsule in a Jail is a good way to learn both at the same time.

## Installing FreeBSD on a RaspberryPi

Installing FreeBSD on a RaspberryPi is relatively easy, [downloading the FreeBSD 13 RPI image](https://download.freebsd.org/ftp/releases/arm64/aarch64/ISO-IMAGES/13.0/) and booting from the SD card to get started. Everything will come up automatically, and you can ssh in with the default user:pass of `freebsd:freebsd`.

A few post-install things I did to secure the host more,

* Add another non-root user other than `freebsd`
* Disable password logins and require ssh-keys
* Setup [doas](https://man.openbsd.org/doas) for new user
* Remove the `freebsd` user with `doas rmuser freebsd`
* Set strong root password

## Setting up NTP

Since the RPI doesn't have a real-time clock, setting up NTP is crucial for accurate time, which if not set can cause all sorts of issues with TLS and other commands.

```shell
# Enabe ntpd
host$ echo 'ntpd_enable="YES"' | doas tee -a /etc/rc.conf

# Force sync time
host$ doas ntpdate pool.ntp.org

# Start ntpd
host$ doas service ntpd onestart
```

## Setting up the Jail

### Creating the Jail

The [Jails guide](https://docs.freebsd.org/en/books/handbook/jails/) is straightforward, but contains two different methods of configuring jails. The built-in `jail` commands or `ezjail`. I ended up [using ezjail](https://docs.freebsd.org/en/books/handbook/jails/#jails-ezjail) which seems more robust and featureful.

Following the instructions first add the second loopback interface,

```shell
host$ echo 'cloned_interfaces="lo1"' | doas tee -a /etc/rc.conf
host$ doas service netif cloneup
```

Then install ezjail and a few other packages we'll need later on,

```shell
host$ doas pkg install ezjail ca_root_nss openssl
host$ echo 'ezjail_enable="YES"' | doas tee -a /etc/rc.conf
```

Create a new jail named `thesours`, using the new second loopback and a new LAN IP on the interface `em0`,

```shell
host$ doas ezjail-admin create thesours 'lo1|127.0.1.1,em0|192.168.7.223'
```

This installs a FreeBSD 13 (default version is the host version) jail filesystem in `/usr/jails/thesours/` and will take a while to download and extract.

Once complete, list the new jail,

```shell
host$ doas ezjail-admin list
STA JID  IP              Hostname                       Root Directory
--- ---- --------------- ------------------------------ ------------------------
DR  1    127.0.1.1       thesours                       /usr/jails/thesours
    1    ue0|192.168.7.223
```

### Setting up the Jail

Now that there's a running jail, connect to it's console to start setting it up.

```shell
doas ezjail-admin console thesours
```

Many of the directories are shared with the basejail and are immutable, but adding users and packages, configuring services, and `/etc` are all independent of the host OS.

Add a new non-root user using `adduser`, install `doas` and set up this user for root privileges. Enabling `sshd` also allows ssh sessions into the jail,

```shell
jail$ echo 'sshd_enable="YES"' | doas tee -a /etc/rc.conf
```

### Setting up a Gemini Capsule

Now that the jail is setup, the next step is installing and configuring the Gemini server [Molly Brown](https://tildegit.org/solderpunk/molly-brown), which has a lot of features such as `~` support for user gemini folders and SCGI/CGI scripting.

#### Building Molly Brown

Molly Brown requires `go`, which was built in the host and not the jail in order to keep jail packages to a minimum.

```shell
host$ doas pkg install go
```

Build Molly Brown,

```shell
host$ mkdir ~/go
host$ export GOPATH=~/go
host$ go get tildegit.org/solderpunk/molly-brown
```

Copy the resulting `~/go/bin/molly-brown` binary to the jail,

```shell
host$ doas cp molly-brown /usr/jails/thesours/usr/local/sbin/
```

Also create the TLS certs that molly brown will require later, and copy them to the jail,

```shell
host$ doas mkdir -p /usr/jails/thesours/etc/ssl/gemini/
host$ cd /usr/jails/thesours/etc/ssl/gemini/
host$ openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 1826 -nodes -subj '/CN=thesours.ecliptik.com'
```

Go back into the jail and setup a few configurations for Molly Brown with the following assumptions,

* Config in `/etc/molly.conf`
* Logs in `/var/log/molly`
* TLS certs in `/usr/jails/thesours/etc/ssl/gemini`
* Document root in `/var/gemini/`
* Run as `daemon`

Create the required paths, create/copy files and set the proper permissions for `daemon`,

```shell
jail$ doas mkdir -p /var/log/molly /var/gemini/
jail$ doas chown -R daemon:daemon /var/log/molly /usr/jails/thesours/etc/ssl/gemini /var/gemini/
```

#### Molly Brown Configuration

Create  configuration in `/etc/molly.conf`,

```shell
## Molly basic settings
Port = 1965
Hostname = "thesours.ecliptik.com"
CertPath = "/etc/ssl/gemini/cert.pem"
KeyPath = "/etc/ssl/gemini/key.pem"
DocBase = "/var/gemini/"
HomeDocBase = "users"
GeminiExt = "gmi"
DefaultLang = "en"
AccessLog = "/var/log/molly/access.log"
ErrorLog = "/var/log/molly/error.log"
```

#### Creating a Molly Brown Service

Create `etc/rc.d/molly` to manage the service and have it start when the jail does. It will run as the `daemon` user to improve security.

```shell
#!/bin/sh
#
# $FreeBSD$
#

# PROVIDE: molly
# REQUIRE: networking
# KEYWORD: shutdown

. /etc/rc.subr

name="molly"
desc="Gemini Protocol daemon"
rcvar="molly_enable"
command="/usr/local/sbin/molly-brown"
command_args="-c /etc/molly.conf"
molly_brown_user="daemon"
pidfile="/var/run/${name}.pid"
required_files="/etc/molly.conf"

start_cmd="molly_start"
stop_cmd="molly_stop"
status_cmd="molly_status"

molly_start() {
        /usr/sbin/daemon -P ${pidfile} -r -f -u $molly_brown_user $command
}

molly_stop() {
        if [ -e "${pidfile}" ]; then
                kill -s TERM `cat ${pidfile}`
        else
                echo "${name} is not running"
        fi

}

molly_status() {
        if [ -e "${pidfile}" ]; then
                echo "${name} is running as pid `cat ${pidfile}`"
        else
                echo "${name} is not running"
        fi
}

load_rc_config $name
run_rc_command "$1"
```

Enable the service,

```shell
jail$ echo 'molly_enable="YES"' | doas tee -a /etc/rc.conf
```

Add a default `/var/gemini/index.gmi` file with some basic gemtext and start the `molly` service,

```shell
jail$ doas service molly start
```

### Running Example

The gemini capsule [gemini://thesours.ecliptik.com](gemini://thesours.ecliptik.com) is running Molly Brown in a FreeBSD jail.
