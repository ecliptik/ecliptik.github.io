---
layout: post
title: Surfing GlobalTalk with a Macintosh 512Ke
category: macintosh
tags: marchintosh globaltalk macintosh localtalk 512ke appletalk
---

While I've discussed the [origins of my Macintosh 512Ke](https://www.ecliptik.com/A-Macintosh-Story/) and the [enhancements](https://www.ecliptik.com/Enhancing-my-Macintosh-512Ke/) I've done over the past year. What really kicked off my interest in using it more than just Zoom background discussion piece, were all the fediverse posts I saw on [GlobalTalk](https://marchintosh.com/globaltalk.html) during [MARCHintosh](https://www.marchintosh.com/) 2024.

I was intrigued that classic Macs like my 512Ke, which I always thought was limited in what it could do, could network with other systems, and not just locally but globally. With this in mind I set a goal for myself to have my 512Ke participate in GlobalTalk for MARCHintosh 2025.

## LocalTalk, GlobalTalk, TashTalk, Oh My

A quick aside, as noted in my [512Ke enhancements](https://www.ecliptik.com/Enhancing-my-Macintosh-512Ke/) post,I swapped a Macintosh Plus logic board for the 512Ke board in the original case. By using a PicoPSU, RGB2HDMI, FloppyEMU, an original mouse and PS2 keyboard adapter, I can run the 512Ke in a bareboard cyberpunk fashion.

[![Bareboard 512Ke](/assets/images/posts/512ke/512ke-bareboard.jpg){: width="60%"}](/assets/images/posts/512ke/512ke-bareboard.jpg)
<figure><figcaption>Bareboard 512Ke</figcaption></figure>

To get my 512Ke onto GlobalTalk, I first physically connected everything using [PhoneNET](https://en.wikipedia.org/wiki/PhoneNET) with the following hardware,

- [TashTalk 2 HAT](https://ko-fi.com/s/4d01fa5b8a) on a RaspberryPi 3
- Original Farrallon PhoneNET adapter connected to the TashTalk 2 HAT
- [Tashtari PhoneNET Adapter](https://ko-fi.com/s/ce23779f25) connected to the 512Ke

[![TashTalk 2 HAT](/assets/images/posts/512ke/tashtalk2.jpg){: width="60%"}](/assets/images/posts/512ke/tashtalk2.jpg)
<figure><figcaption>TashTalk 2 HAT on a RaspberryPi 3</figcaption></figure>

[![Farrallon PhoneNET adapter](/assets/images/posts/512ke/farrallon.jpg){: width="60%"}](/assets/images/posts/512ke/farrallon.jpg)
<figure><figcaption>Farrallon PhoneNET</figcaption></figure>

[![Tashtari PhoneNET Adapter](/assets/images/posts/512ke/db9adapter.jpg){: width="60%"}](/assets/images/posts/512ke/db9adapter.jpg)
<figure><figcaption>Tashtari PhoneNET Adapter</figcaption></figure>

## Networking

With everything physically connected, in order for the TashTalk HAT to see LocalTalk traffic, the networking on the RaspberryPi must be setup with a bridge and tap device. Taking inspiration from a [post on m68kmla](https://68kmla.org/bb/index.php?threads/tashrouter-an-appletalk-router.46047/page-5#post-518796) I configured the host networking as follows.

Install required bridge and tap packages,

```sh
sudo apt install uml-utilities bridge-utils
```

Configured `/etc/network/interfaces` with a bridge, tap and static IP address,

```
#loopback
auto lo
iface lo inet loopback

# Virtual interface
auto tap2
iface tap2 inet manual
   pre-up tunctl -t tap2 -u root
   up ip link set dev tap2 up
   down ip link set dev tap2 down

# Bridge interface
auto br0
iface br0 inet static
   address 192.168.1.163/24
   gateway 192.168.1.1
   dns-nameservers 192.168.1.1
   bridge_ports eth0 tap2
   bridge_fd 9
   bridge_hello 2
   bridge_maxage 12
   bridge_stp off
```

Disabled NetworkManager since I want to use `/etc/network/interfaces` for network configuration,

```sh
sudo systemctl disable NetworkManager
```

After restarting the Pi, the eth0 and tap interfaces will show up on `br0` bridge,

```sh
sudo brctl show
bridge name     bridge id               STP enabled     interfaces
br0             8000.ae29d573875f       no              eth0
                                                        tap2
```

## TashRouter

Using the tap2 device, next is bridging the TashTalk 2 HAT to Ethernet, making [LocalTalk](https://en.wikipedia.org/wiki/LocalTalk) traffic visible on the wider network. This is done using [tashrouter](https://github.com/lampmerchant/tashrouter) which communicates with the TashTalk 2 HAT on `/dev/ttyAMA0` and passes LocalTalk to LToUDP and [EtherTalk](https://apple.fandom.com/wiki/EtherTalk) through the tap2 device.

Using the example from the tashrouter repo, I created `gt_router.py` python script, changing the `seed_zone_name` to `Vermilion Sands LT`. This is important, since if LocalTalk devices are in the same Zone as EtherTalk devices it can cause some odd [AppleTalk](https://en.wikipedia.org/wiki/AppleTalk) behaviour like file servers not showing up.

`gt_router.py`
```python
import logging                                                                                                                                 import time
import signal                                                                                                                                  import sys

import tashrouter.netlog
from tashrouter.port.ethertalk.tap import TapPort
from tashrouter.port.localtalk.ltoudp import LtoudpPort
from tashrouter.port.localtalk.tashtalk import TashTalkPort
from tashrouter.router.router import Router

def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
#tashrouter.netlog.set_log_str_func(logging.debug)  # comment this line for speed and reduced spam

router = Router('router', ports=(
  LtoudpPort(seed_network=71, seed_zone_name=b'Vermilion Sands LT'),
  TashTalkPort(serial_port='/dev/ttyAMA0', seed_network=72, seed_zone_name=b'Vermilion Sands LT'),
  TapPort(tap_name='tap2', hw_addr=b'\xDE\xAD\xBE\xEF\xCA\xFE'),
))
print('router away!')
router.start()
signal.signal(signal.SIGTERM, sigterm_handler)

try:
  while True: time.sleep(1)
except (KeyboardInterrupt, SystemExit):
  router.stop()
```

This script is run with `sudo python3 gt_router.py`.

## An On-ramp to The Information Superhighway

With LocalTalk bridged into the Ethernet network, next is getting onto GlobalTalk.

I first followed the [The Ultimate GlobalTalk Network Guide](https://docs.google.com/document/d/1pXMjrAF5vC08TamkdSt2oFCrDFMP47i5dYcjshn9JzU/edit?tab=t.0) to understand how things worked, however this guide uses the older [AppleTalk Router](https://biosrhythm.com/?p=2767) software that runs only on a Macintosh system, not Linux.

The newer [jrouter](https://gitea.drjosh.dev/josh/jrouter) project runs on Linux and has features like yaml configuration, logs, and can integrate with tashrouter using the bridge setup.

My configuration for jrouter uses the `br0` bridge device, sets the zone name `Vermilion Sands`, a 1970-1971 network range and opens up peering. The list of peers was copied from the GlobalTalk spreadsheet. As mentioned before, it's important the `zone_name` and network range differ from the LocalTalk zone name.

`jrouter.yaml`
```yaml
listen_port: 387 #AURP default port
local_ip: XX.XX.XX.XX #Public IP to forward traffic from
monitoring_addr: ":9459"
ethertalk:
  - device: br0
    zone_name: Vermilion Sands
    net_start: 1970
    net_end: 1971
open_peering: true
peers:
    - #peer IPs from GlobalTalk spreadsheet
```

By using the same `br0` bridge device as the `gt_router.py` script, LocalTalk devices will see GlobalTalk devices and vice versa.

## Putting it All Together

With the hardware and software taken care of, everything was in place to start browsing GlobalTalk on the 512Ke like it was 2024. Through various trial and error, I found there is a specific order-of-operations needed for everything to work as expected.

1. Turn everything off
2. Physically connect everything
3. Turn on RaspberryPi
4. Start jrouter and wait a few minutes for zone information to populate
5. Start `gt_router.py`
6. Turn on clients, like the 512Ke

When running properly, `gt_router.py` logs will show GlobalTalk traffic and zones and file servers will appear in Chooser on the 512Ke.

[![512Ke About System showing GlobalTalk Zones](/assets/images/posts/512ke/screenshot-512ke-about.png)](/assets/images/posts/512ke/screenshot-512ke-about.png)
<figure><figcaption>512Ke About System with GlobalTalk Zones</figcaption></figure>

[![512Ke Chooser showing GlobalTalk Zones](/assets/images/posts/512ke/screenshot-512ke-chooser.png)](/assets/images/posts/512ke/screenshot-512ke-chooser.png)
<figure><figcaption>GlobalTalk Zones in Chooser on 512Ke</figcaption></figure>

## Gotchas

Here are a few gotchas I came across when configuring everything.

- If running [netatalk](https://netatalk.io/) or a QEMU Macintosh, put them on a different system than jrouter/tashtalk. Having them all share the same `br0` device causes some sort of network loop and can crash a Macintosh connected with LocalTalk.

- When in doubt turn everything off and back on again. AppleTalk is temperamental, zones and file servers will just disappear or stop working even though nothing changed. Sometimes the best course of action is to turn everything off, wait a few minutes and then back on again.

- Patience is a virtue. The technologies and bitrates involved as relatively slow, and sometimes it just requires waiting a few extra seconds instead of expecting everything to function immediately.

## Stretch Goal

A stretch goal I had for this project was seeing if I could transfer files between my 512Ke and a modern Macbook using LocalTalk. I managed to do this by setting up a [netatalk 4.1](https://netatalk.io/) server on another RaspberryPi with AppleTalk enabled. Because netatalk is able to join the AppleTalk network, it can see and make available it's services to all devices, including the 512Ke.

After setting up a file share on netatalk, the 512Ke can mount it in Chooser over LocalTalk and Finder on MacOS will see it over wifi. Now I can easily copy files (albeit slowly) between systems using this shared folder.

[![Screenshot of 512Ke, netatalk cli and MacOS of the same directory and files](/assets/images/posts/512ke/512ke-netatalk-macos.png)](/assets/images/posts/512ke/512ke-netatalk-macos.png)
<figure><figcaption>File share on a 512Ke, Finder and Linux</figcaption></figure>

[![Rough diagram of how everything is connected](/assets/images/posts/512ke/globaltalk-diagram.png)](/assets/images/posts/512ke/globaltalk-diagram.png)
<figure><figcaption>Rough diagram of how everything is connected</figcaption></figure>


## References and Links

- [Pushing AppleTalk Across the Internet](https://biosrhythm.com/?p=2767)
- [GlobalTalk Virtual Router on Debian 12](https://globaltalk.woodlanddigital.net/qemu/)
- [TashRouter: An AppleTalk Router](https://68kmla.org/bb/index.php?threads/tashrouter-an-appletalk-router.46047/)
- [The Ultimate GlobalTalk Network Guide v1.1](https://docs.google.com/document/d/1pXMjrAF5vC08TamkdSt2oFCrDFMP47i5dYcjshn9JzU/edit?tab=t.0)
- [Welcome to #GlobalTalk!](https://marchintosh.com/globaltalk.html)
- [Using TashTalk with Mini vMac to participate in #GlobalTalk from your emulated Mac](https://blog.vladovince.com/using-tashtalk-with-mini-vmac-to-participate-in-globaltalk-from-your-emulated-mac/)
- [My GlobalTalk Setup: Apple Internet Router configuration](https://blog.vladovince.com/my-globaltalk-setup-1-apple-internet-router-configuration/)
- [Building a Classic Mac Support Server](https://biosrhythm.com/?p=2791)
- [Notes From Setting up GlobalTalk Using QEMU on Ubuntu](https://midnightcheese.com/2025/03/notes-setting-up-globaltalk-qemu-ubuntu/)
- [Macintosh Networking Bookmark Collection](https://midnightcheese.com/2025/03/notes-setting-up-globaltalk-qemu-ubuntu/)
