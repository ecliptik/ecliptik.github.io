---
layout: post
title: DNS Guardrails with dnscrypt-proxy
category: linux
tags: linux dns containers docker networking tailscale
---

## Intro

Over the holidays we got our two younger children HP laptops for them to do their school work on and to have a proper computer. While the schools Google Classroom login effectively adds restrictions to Chrome, I still wanted to have some guardrails on their Internet access as well as ad-blocking.

The first thing I did was replace the Windows S install that came on the laptops with [Linux Mint](https://www.linuxmint.com/) as I've always enjoyed the [Cinnamon desktop environment](https://projects.linuxmint.com/cinnamon/) and it has a low enough learning curve that the kids could easily pick it up. After installing a few apps and games ([OpenRCT2](https://openrct2.org/)) from the Software Center and setting their own passwords, they were up and running and surfing the world-wide-web.

Finally I added [Tailscale](https://tailscale.com/) to both laptops to put them on my [tailnet](https://tailscale.com/kb/1136/tailnet). This has benefits of accessing tailnet-only services, easier remote access, and leveraging the [dnscrypt-proxy on OpenBSD](https://www.ecliptik.com/Running-dnscrypt-proxy-on-OpenBSD/) I setup a few years ago for DNS.

## Guardrails

My original DNS config worked well, but I wanted to add some guardrails specifically for the kids laptops,

1. [Cloudflare for Families](https://blog.cloudflare.com/introducing-1-1-1-1-for-families/)
2. [Ad Blocking](https://github.com/DNSCrypt/dnscrypt-proxy/wiki/Public-blocklist)
3. [YouTube Restricted Mode](https://support.google.com/a/answer/6212415) via [Cloaking](https://github.com/DNSCrypt/dnscrypt-proxy/wiki/Public-blocklist)
4. Accessible only from the Tailscale

First I tried using the existing [dnscrypt-proxy](https://github.com/DNSCrypt/dnscrypt-proxy) to provide a different set of DNS resolvers depending on the source IP, but this wasn't possible. Eventually I came up with a seperate DNS infrastructure in a container for the laptops to use,

## Container Stack

`Dockerfile` is used for building a container including `dnscrypt-proxy`,

```dockerfile
FROM debian:trixie-slim
ENV DEBIAN_FRONTEND noninteractive

RUN apt update && \
    apt install -y dnscrypt-proxy \
      ca-certificates \
    && apt clean

WORKDIR /tmp
ENTRYPOINT [ "/usr/sbin/dnscrypt-proxy" ]
CMD [ "-config", "/etc/dnscrypt-proxy/dnscrypt-proxy.toml" ]
```

[docker compose](https://docs.docker.com/compose/) is used to bring up the stack, which includes a `tailscale` container to provide network and access to other devices on the tailnet. Configuration files are monted read-only from the current directly and some volumes to maintain state across restarts.

`docker-compose.yml`

```yaml
version: '3.9'
services:
  tailscale:
    container_name: tailscale-dnscrypt
    hostname: dnscrypt-proxy
    image: ghcr.io/tailscale/tailscale
    stdin_open: true
    environment:
      - TS_AUTH_KEY=${TS_AUTH_KEY}
      - TS_USERSPACE=true
      - TS_STATE_DIR=/var/lib/tailscale
      - TS_SOCKET=/var/run/tailscale/tailscaled.sock
    volumes:
      - dnscryptvarlib:/var/lib
    restart: unless-stopped
  dnscrypt-proxy:
    build: .
    stdin_open: true
    volumes:
      - ./dnscrypt-proxy.toml:/etc/dnscrypt-proxy/dnscrypt-proxy.toml:ro
      - ./blocklist.txt:/etc/dnscrypt-proxy/blocklist.txt:ro
      - ./cloaking-rules.txt:/etc/dnscrypt-proxy/cloaking-rules.txt:ro
      - ./domains-allowlist.txt:/etc/dnscrypt-proxy/domains-allowlist.txt:ro
      - keys:/etc/dnscrypt-proxy/keys
    restart: unless-stopped
    network_mode: 'service:tailscale'
volumes:
  dnscryptvarlib:
  keys:
```

## dnscrypt-proxy

The dnscrypt-proxy configuration uses the `cloudflare-family` source and ad-blocking using a `blocklist.txt` generated with [generate-domains-blocklist.py](https://github.com/DNSCrypt/dnscrypt-proxy/wiki/Combining-Blocklists). All logs go to `/dev/stdout` so they appear in `docker compose logs`.

`dnscrypt-proxy.toml`

```toml
#Use cloudflare DNS
server_names = ['cloudflare-family']

#Listen on local and LAN addresses for DNS
listen_addresses = ['127.0.0.1:53']
max_clients = 250
user_name = '_dnscrypt-proxy'

#Enable ipv4 and ipv6
ipv4_servers = true
ipv6_servers = false

#Allow TCP and UDP
force_tcp = false
timeout = 2500
keepalive = 30

#Logging
log_level = 2
use_syslog = true

#Certs
cert_refresh_delay = 240
dnscrypt_ephemeral_keys = true
tls_disable_session_tickets = true

#Cache
cache = true

#Cloaking
cloaking_rules = '/etc/dnscrypt-proxy/cloaking-rules.txt'

#Query logging, commented out unless for troubleshooting
[query_log]
  file = '/dev/stdout'
  format = 'tsv'

#Sources for resolvers and relays
[sources]
  [sources.'public-resolvers']
  urls = ['https://raw.githubusercontent.com/DNSCrypt/dnscrypt-resolvers/master/v3/public-resolvers.md', 'https://download.dnscrypt.info/resolvers-list/v3
/public-resolvers.md']
  minisign_key = 'RWQf6LRCGA9i53mlYecO4IzT51TGPpvWucNSCh1CBM0QTaLn73Y7GFO3'
  cache_file = '/var/tmp/public-resolvers.md'
  refresh_delay = 72

#Blocking configuration
[blocked_names]
  ## Path to the file of blocking rules (absolute, or relative to the same directory as the executable file)
  blocked_names_file = '/etc/dnscrypt-proxy/blocklist.txt'
  log_file = '/dev/stdout'
  log_format = 'tsv'

#Allow configuration
[allowed_names]
  allowed_names_file = '/etc/dnscrypt-proxy/domains-allowlist.txt
```

[Cloaking](https://github.com/DNSCrypt/dnscrypt-proxy/wiki/Public-blocklist) is used so all YouTube requests resolve to `restrict.youtube.com`.

`cloaking-rules.txt`

```txt
www.youtube.com restrict.youtube.com
m.youtube.com  restrict.youtube.com
youtubei.googleapis.com restrict.youtube.com
youtube.googleapis.com restrict.youtube.com
www.youtube-nocookie.com restrict.youtube.com
```

## Exposing via Tailscale

Since I only want DNS available to devices on my tailnet, and not publicly available, there's a `tailscale` container in the `docker-compose.yml` that provides networking to the `dnscrypt-proxy` container using `network_mode`.

Set this up by creating an [auth key](https://tailscale.com/kb/1085/auth-keys) for your tailnet and then putting it into a `.env` file that docker compose will source in and set as the `TS_AUTH_KEY` variable.

`.env`

```shell
TS_AUTH_KEY=tskey-auth-xxxxxxxxxxx
```

## Enabling on Linux Mint

My tailnet uses [Magic DNS](https://tailscale.com/kb/1081/magicdns) which sets the nameserver for all devices on a tailnet to `100.100.100.100`, but since this is a DNS server specific to a subset of systems we want to use the IP of the `dnscrypt-proxy` device instead.

After bringing up the stack with `docker compose up`, the `tailscale` container will authenticate to the tailnet and have an Tailscale IP (eg `100.112.129.40`). This IP is then added to the laptops `/etc/resolv.conf`,

```
nameserver 100.112.129.40
search tailnet-3831.ts.net
```

Tailscale will keep trying to revert this, so to keep the settings permanent, `/etc/resolv.conf` is set to immutable with `chattr +i /etc/resolv.conf`.

To test DNS is working, looking for more "adult" content on youtube will give a message similar to "your Google workspace administrator has restricted some content".

Verify in container logs with `dig m.youtube.com  @100.76.233.91` (where the IP is your Tailscale container IP) and check the logs for messages similar to `127.0.0.1       m.youtube.com   A       CLOAK   0ms     -`.
