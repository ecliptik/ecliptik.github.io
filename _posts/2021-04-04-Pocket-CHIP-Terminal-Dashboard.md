---
layout: post
title: Pocket CHIP Terminal Dashboard
category: chip
tags: chip hack 100daystooffload
toc: true

comments:
  show:  true
  fediHost:  fosstodon.org
  fediusername:  ecliptik
  fediid:  106011231236382834

---

## Intro

When I first got my [Pocket C.H.I.P.](https://www.ecliptik.com/Pocket-CHIP/) one of the first thoughts I had was to use it as sort of a mini-desktop terminal to display things like weather, new mail, etc. After doing some [other tinkering](https://www.ecliptik.com/CHIP-Serial-Console/) with it first, it has been on my desk the last couple of weeks displaying the following information,

* Latest local toot in [Fosstodon](https://fosstodon.org/web/timelines/public/local) using [Toot](https://github.com/ihabunek/toot)
* Top 10 [Hacker News](https://news.ycombinator.com) posts using [haxor-news](https://github.com/donnemartin/haxor-news)
* Current weather from [wttr.in](https://wttr.in)
* Current time with [tty-clock](https://github.com/xorg62/tty-clock)
* Currenly playing track on Spotify using [walt-grover](https://github.com/ecliptik/walt-grover)

![Pocket C.H.I.P Terminal Dashboard](/assets/images/posts/chip_terminal/IMG_6909.png)
<figure><figcaption>Pocket C.H.I.P. Terminal Dashboard</figcaption></figure>

## Setup

[Tmux](https://github.com/tmux/tmux) is the heart of the setup, with each applet in it's own terminal pane and then borders turned off so it looks like a single seamless screen. Running in tmux has the added benefit of detaching the dashboard, like when you want to watch some [vaporwave on the framebuffer](https://www.ecliptik.com/CHIP-Vaporwave/) or sharing the screen from ssh for remote control.

The tools used in these panes are a combination of `watch` to refresh every 60 seconds or a small shell script. I attempted to use `watch` for everything, but some commands didn't work well with the ASCII escape codes even with the `--color` option.

It's using [tmuxinator](https://github.com/tmuxinator/tmuxinator) to save the layout and restore the dashboard after a reboot.

Tmuxinator config in `~/.config/tmuxinator/chip.yaml`

```
name: chip
root: ~/

windows:
  - CHIP:
      layout: 7bd9,60x33,0,0[60x7,0,0,0,60x13,0,8,3,60x7,0,22{27x7,0,22,4,32x7,28,22,9},60x3,0,30,6]
      panes:
        - watch -n60 -t --color "toot timeline --local --public --count 1 --once | sed '/^$/d' | grep -v '─────────────────' | grep -v 'ID ' | sed 's/\s\{2,\}/_TOKEN_/' | awk -F_TOKEN_ {'print \$1'}"
        - watch -n60 -t --color "hn top 10 | head -n -3 | sed 's/^[ \t]*//' | grep -v 'points by' | awk -F\( {'print \$1'} | sed -e 's/\.\s\s\s/. /g'"
        - /home/chip/bin/weather.sh
        - bin/tty-clock -m -B -D -C 5
        - watch -n120 -t --color "/home/chip/bin/spotify/spotify.rb"
  - amfora:
      - amfora
  - serial:
```
Additional configuration includes updating the [pocketchip-batt](https://github.com/aleh/pocketchip-batt) utility to better display charging and how much battery is remaining and putting it and the CHIPs IP address into the right status of the tmux toolbar.

Terminal blanking is turned off so the display is always on.

```
setterm -blank 0
```

Wifi powersave feature is turned off since there were issues with it losing DNS and occasional loss of network connectivity

```
sudo /sbin/iw dev wlan0 set power_save off
```

Tmux config in `~/.tmux.conf`,

```
#Switch Windows
bind-key n next-window
bind-key m previous-window

#Set 256 colors
set -g default-terminal "screen-256color"

# start window numbering at 1
set -g base-index 1

# start pane numbering at 1
set -g pane-base-index 1

#Update default binding of `Enter` to also use copy-pipe
unbind -T copy-mode-vi Enter

#Clock
set-option -g clock-mode-colour yellow

#Switch panels with vi keybindings
bind k selectp -U # switch to panel Up
bind j selectp -D # switch to panel Down
bind h selectp -L # switch to panel Left
bind l selectp -R # switch to panel Right

set-option -g status on
set-option -g status-interval 1
set-option -g status-keys vi
set-option -g status-position bottom

set-option -g visual-activity on
set-window-option -g status-left ""
set-window-option -g monitor-activity on
set-window-option -g window-status-activity-style "none"
set-option -g status-right "#( ~/bin/right-status.sh )"

#### COLOUR (Solarized light)

# default statusbar colors
set-option -g status-style fg=yellow,bg=black #yellow and base02

# default window title colors
set-window-option -g window-status-style fg=brightblue,bg=default #base0 and default
#set-window-option -g window-status-style dim

# active window title colors
set-window-option -g window-status-current-style fg=brightred,bg=default #orange and default
#set-window-option -g window-status-current-style bright

# pane border
set-option -g pane-border-style fg=black #base02
set-option -g pane-active-border-style fg=black #base01

# message text
set-option -g message-style fg=brightred,bg=black #orange and base01

# pane number display
set-option -g display-panes-active-colour blue #blue
set-option -g display-panes-colour brightred #orange

# clock
set-window-option -g clock-mode-colour green #green

# bell
set-window-option -g window-status-bell-style fg=black,bg=red #base02, red
```
