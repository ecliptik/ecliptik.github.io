---
layout: post
title: Switching to Ghostty
category: linux
tags: terminal shell linux macos zsh bash
---

## Ghostty

In December 2024 the new terminal emulator [ghostty](https://ghostty.org/) created by mitchellh[](https://mitchellh.com/) (founder of [Hashicorp](https://www.hashicorp.com/)) was released.

I originally had the (incorrect) assumption that it was similar to other "new" terminal emulators that require a network connection, were built in javascript or had some sort of "AI" features wedge in.

What caught my eye though when reading [About Ghostty](https://ghostty.org/docs/about), was the focus on the following,

- [Native](https://ghostty.org/docs/about#native) no Electron
- [Fast](https://www.youtube.com/watch?v=cPaGkEesw20&t=3015s)
- [Released when Ready]( https://mitchellh.com/writing/ghostty-is-coming)

This quote by mitchellh and finally convinced me I should give it a try,

>I like to imagine that if stores like CompUSA still existed, Ghostty 1.0 would be boxed, shrink-wrapped, and on the shelf ready for purchase (but also free and open-source).

![My Ghostty Terminal editing a draft of this post](/assets/images/posts/ghostty/ghostty-terminal.png)
<figure><figcaption>Ghostty Terminal</figcaption></figure>

## Initial Impressions

Installing on my MacOS and Linux laptops was relatively straightforward, although for my [Linux Mint](https://linuxmint.com/) laptop I had to install a .deb from a [3rd party repo](https://github.com/mkasberg/ghostty-ubuntu). What I first noticed was it's sane defaults, it just worked out-of-the-box and I could just start using it. It was snappy too, especially compared to Terminal.app on my MacOS.

What really hooked me was finding the [built-in themes](https://ghostty.org/docs/features/theme), including my current favorite, [Tokyo Night](https://github.com/tokyo-night/tokyo-night-vscode-theme). Not only were these built into ghostty, but there was an interactive preview feature with the `ghostty +list-themes` command.

![Ghostty Theme Preview](/assets/images/posts/ghostty/ghostty-preview.png)
<figure><figcaption>Ghostty Theme Preview</figcaption></figure>

It was a lot of fun previewing themes with zero friction of trying them out, unlike other terminal emulators where you have to change a config and then reload it. In addition, the `theme` options can set a theme for both light and dark modes, dynamically switching depending on your OS setting. I like to have a "light" OS theme during the day and a "dark" theme during the night and this was a feature I haven't seen in other terminal emulators.

## Customizing the Config

My ghostty configuration is relatively small, with a few changes for how I like my terminal emulator,

- [TX-02](https://usgraphics.com/products/berkeley-mono)(Berkeley Mono) Font
- Semi-transparent blurred background
- Block style blinking cursor
- Inverted selection
- Easy to read

`~/.config/ghostty/config`
```
#Font
font-family = "TX-02"
font-size = "16"

#Terminal settings
term = "xterm-256color"

#Visuals
theme = "light:tokyonight-day,dark:tokyonight"
background-opacity = .9
background-blur-radius = 20
selection-invert-fg-bg = true
bold-is-bright = true
minimum-contrast = 2

#Cursor
cursor-style = block
cursor-style-blink = true
cursor-invert-fg-bg = true
cursor-opacity = .8
shell-integration-features = no-cursor
```

## Graphics

I've always though it was cool that some terminals could display graphics using [sixels](https://en.wikipedia.org/wiki/Sixel), but support in Terminal.app was never there. Ghostty doesn't support sixels either, but does support the [Kitty Graphics Protocol](https://sw.kovidgoyal.net/kitty/graphics-protocol/), which is even better as it's a modern library and in active development.

This lets terminals tools like `timg`, `mpv` and `neofetch` display graphics right in the terminal.

![Ghostty Graphics](/assets/images/posts/ghostty/ghostty-graphics.png)
<figure><figcaption>Ghostty Graphics</figcaption></figure>

## After Two Weeks

I've been using ghostty for the past two weeks on all my systems and I've really enjoyed it. It performs much better than Terminal.app on MacOS, which feels extremely sluggish in comparison now.

That's not to say I haven't had any issues,

- Somehow Super+Shift+V makes it impossible in `vim` to switch out of insert mode
- Background blur was just recently added for Linux, but isn't in an official release yet
- On MacOS the cursor will not change depending on the context (issue [3257](https://github.com/ghostty-org/ghostty/discussions/3257))

These aren't enough to keep from using ghostty, and I am looking forward to what future releases have in store.
