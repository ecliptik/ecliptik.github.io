---
layout: post
title: Superhighway84 on FreeBSD
category: bsd
tags: freebsd smolweb ipfs

comments:
  show:  true
  fediHost:  fosstodon.org
  fediusername:  ecliptik
  fediid:  107642122120401193

---

A couple of weeks ago I saw [Superhighway84](https://マリウス.com/superhighway84/) on [HackerNews](https://news.ycombinator.com/item?id=28453165) and started to check it out, but didn't get very far. I finally spent some time to get it up and running on [FreeBSD](https://www.freebsd.org) which works, but requires a few additional steps.

I wanted to get Superhighway84 on a spare RaspberryPi 3 running FreeBSD 13, primarily used for a [Gemini Capsule in FreeBSD](https://www.ecliptik.com/Gemini-Capsule-in-a-FreeBSD-Jail/), since it doesn't have much traffic and is mostly idle.

> Superhighway84 is an USENET-inspired decentralized internet discussion system, featuring a retro text user interface and powered by IPFS and OrbitDB.

![Superhighway84](/assets/images/posts/superhighway84/superhighway84.png)
<figure><figcaption>Superhighway84 in Solarized Dark terminal</figcaption></figure>

## IPFS on FreeBSD

Superhighway84 uses [IPFS](https://ipfs.io) as it's backend, making it fully decentralized. Reading through the setup docs, an `ipfs init` is required to build the initial `~/.ipfs` filesystem. There is a [ipfs-go](https://www.freshports.org/sysutils/ipfs-go/) in FreeBSD ports, but it doesn't seem to work, at least on arm64.

To work around this, building [ipfs-go](https://github.com/ipfs/go-ipfs) from source is doable in a few steps,

First, install a few required packages to compile the `go` binaries

```shell
$ doas pkg install gcc gmake go openssl
```

Next, clone the source of `go-ipfs` and checkout the latest stable branch, otherwise there might be a version mismatch error on startup,
```shell
$ git clone https://github.com/ipfs/go-ipfs.git
$ cd go-ipfs
$ git checkout tags/v0.11.0
```

Set a few environment vars to compile with `gcc` and use `openssl`,

```shell
$ export PATH=$PATH:/usr/local/go/bin
$ export PATH=$PATH:$GOPATH/bin
$ export CGO_ENABLED=1
$ export GOTAGS=openssl
```

Build from source using `gmake`

```shell
$ doas gmake install
go version go1.17.5 freebsd/arm64
bin/check_go_version 1.15.2
plugin/loader/preload.sh > plugin/loader/preload.go
go fmt plugin/loader/preload.go >/dev/null
go install "-asmflags=all='-trimpath='" "-gcflags=all='-trimpath='" -ldflags="-X "github.com/ipfs/go-ipfs".CurrentCommit=67220edaa" ./cmd/ipfs
```

After the build is finished, copy the binary to `~/bin` and export it into the `$PATH` ,

```shell
$ cp ~/go/bin/ipfs ~/bin
$ export PATH="~/bin:$PATH"
```

Initialize `~/.ipfs` and set profile config to lowpower for running on a RaspberryPi

```shell
$ ipfs init --profile=lowpower
```

## Building Superhighway84

With IPFS initialized, build Superhighway84 and copy the binary to `~/bin`. There are [binary releases](https://github.com/mrusme/superhighway84/releases/tag/v0.0.11) for FreeBSD arm64, but compiling it from source is relatively easy as well.

```shell
$ git clone https://github.com/mrusme/superhighway84.git
$ cd superhighway84
$ go build .
$ cp superhighway64 ~/bin
```

Start up `superhighway84`, and wait a few minutes to fully sync. Using a "light" terminal theme is not recommened as it's difficult to read, and I recommended switching to a darker terminal theme.

```shell
$ superhighway84
```
