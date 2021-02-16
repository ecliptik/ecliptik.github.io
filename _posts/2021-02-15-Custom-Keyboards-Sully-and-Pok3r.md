---
layout: post
title: Custom Keyboards, Sully and Pok3r
category: technology
tags: keyboards technology qmk hardware 100daystooffload

comments:
  show:  true
  fediHost:  fosstodon.org
  fediusername:  ecliptik
  fediid:  105740118192056355
---

Working in the tech industry and having geeky hobbies; I've always taken my tools, both hardware and software, seriously. For some reason I never thought about the keyboard itself though, and was content with using the bundled membrane boards. A few years ago though this all changed which I discovered the deep rabbit hole that is both utilitarian and vain world of custom keyboards.

## Sully

Back in 2013 I convinced my boss that I needed a high-end mechanical keyboard to help with some recent hand pain (almost entirely due to Starbound at the time). I purchased a Coolermaster CM Storm with Cherry MX Green switches. It was my first "small" keyboard in a sense that it was a ten-key-less (TKL) and the green switches were clicky and stiff, exactly what I wanted in a keyboard since it reminded me of the electric typewriters I learned to touch-type on.

After spending some time on [r/MechanicalKeyboards](https://www.reddit.com/r/MechanicalKeyboards/) I got the itch to customize it and bought some blank PBT DSA keys in teal and purple, calling it "Sully".

![Sully](/assets/images/posts/sully.jpg)
<figure><figcaption>Sully</figcaption></figure>

Sully was a fantastic board and I used it up until 2019 when I discovered even smaller form factors like 60%. It's still used in our house, but mostly as a kids toy, demostrating just how well-built it is.

## Vortex Pok3r

The idea of a smaller, 60% board was appealing in with having the same functionality but in a more compact form. Removing some of the less used keys to provide more desk space and limit finger stretch. I also just liked the way it looked, more compact and different than the standard 101 keyboards. I put the Pok3r on my wishlist because it was "programmable" and I had all sorts of ideas on ways I could customize shortcuts and other functions.

It came as a Christmas present in 2019, with Cherry MX blue switches and stock keycaps. I immediately started using the programmable PCB, but found it was much more difficult to do since it involves putting it into programming mode and then keying in what you want to setup. Just remapping some keys, like making CAPS-LOCK -> Escape was an exercise in frustration, but it did what I wanted eventually, with the process meticulously detailed in a .txt file. It also has different layers that could hold different keymaps, but I just stuck with a single layer.

```bash
## Caps-lock as ESC
FN+R_control
CAPS_LOCK
ESC
PN
FN+R_control

## HJKL Navigation
FN+R_Control
FN+H FN+J
FN+J FN+K
FN+K FN+I
PN
FN+R_Control
```
<figure><figcaption>Sample of how to program the stock pok3r firmware</figcaption></figure>

## Pok3r Revived

Eventually I started getting annoyed with the default keycaps, which were a thin cheap ABS plastic and would squeak. Just over a month of use the legends also starting to wear off. This started me down a dark path, first looking into how to stop the squeaking, but then lead to going back to `r/MechanicalKeyboards` and following the white rabbit, and making a wish list to customize the board and make it fully mine.

- Thick PBT Keycaps
- Tactile Switches
- Keyboard Foam
- [QMK Programming Support](https://qmk.fm)

### /dev/tty

The first item on the list was easy enough to do, just scour keyboard stores and find a keycap set. I went through various postings, storefronts, and group buys, eventually landing on [/dev/tty by matt3o](https://matt3o.com/about-mt3-profile-and-devtty-set/). These were particularly attractive because of their story; inspired by [IBM Beamspring terminals](https://www.cannondigi.com/ibm-beamspring-keyboard/) and the `/dev/tty` name.

>MT3 is inspired by old terminal keyboards; TTY was used to refer to "teletype" or "teletypewriter" but it has come to refer to any type of text terminal. As a linux user the temptation to call the set `/dev/tty` was simply too strong to resist.

The MT3 profile is also extremely high, and the deep dish and feel of PBT makes the keys almost "cuddle" your fingertips. Typing on them is an absolutely joy and because of their thickness they sound amazing even on just a stock board.

### Holy Pandas

Next on the list was replacing the switches with something less clicky and more tactile. The original "Sully" board had MX Greens which were extremely clicky and I wanted something different with MX blues in the pok3r, but wanted a change of pace from the last few years. While reading through keyboard sites, the phrase "Holy Panda" kept coming up and how they were fantastic tactile switches. Eventually I came across one of the original post that described the [origins of the Holy Panda](https://topclack.com/textclack/2018/12/19/holy-panda-switches-new-and-old-by-quakemz) and found that it was an entirely custom switch, made from two different switches.

>The Holy Panda switch is the combination of the stem of a Halo True and the housing of a Invyr Panda. The result is the Holy Panda hybrid, one of the snappiest tactile mechanical switches available.

![Pandas](/assets/images/keyboards/pandas.png)
<figure><figcaption>YOK Polar Panda(left) Holy Panda(center) Halo True(right)</figcaption></figure>

The idea of building my own switches really resonated with me since it gave me, giving me more ownership of what I was building. Holy Pandas also sound amazing when typing, not clicky or loud, but thunky and tactile. Pairing them with a thicker PBT keycap set made perfect sense as well.

Luckily I found some YOK Polar Panda switches in-stock and ordered them and some Halo Trues from drop, which created "Polar Holy Pandas" with a distinctive blue housing a salmon stem.

![Building Holy Pandas](/assets/images/keyboards/IMG_4665.png)
<figure><figcaption>Building Holy Pandas</figcaption></figure>

Lubing is also a thing when it comes to building custom switches, and these were lubed with Krytox 205g0, to give them a smoother tactile bump.

### Foam

Did you know you can put foam in a keyboard to help dampen the sound? I had no idea this was a thing, but it is, and it completely changes the sound profile of a keyboard. So if you're into how a keyboard sounds, and are willing to spend 15$, foaming a board is a good investment.

![PCB Foam Sandwich](/assets/images/keyboards/IMG_4706.png)
<figure><figcaption>PCB Foam Sandwich</figcaption></figure>

I opted for foam from [MKUltra](https://mkultra.click/secret-file-cabinet/60-foam/), which I originally thought would go in the bottom of the case. When it arrived I discovered it was plate foam, which goes between the top plate and the PCB, making a sandwich. Even though it wasn't my original choice, it worked much better since now the entire board is a solid piece with exceptional dampening sounds. Combined with the Holy Panda tactile and `/dev/tty` thickness, it makes a satisfying THUNK with every keypress.

### QMK Programming

The last item on the list was improving the programming of the board. I'm planning to write up a more extensive article on [QMK](https://qmk.fm), and the [pok3r can run QMK](https://github.com/pok3r-custom/qmk_pok3r), but requires unlocking the board which is risky and even then will use a fork or QMK and not upstream. While tempted to try this, I found that YMDK makes a drop in replacement [YD60MQ PCB](https://github.com/ecliptik/qmk_firmware/tree/ecliptik/keyboards/yd60mq) that you can buy for under 30$. This also gave me an excuse to get a de-soldering iron to quickly de-solder the switches and not risk damaging them by using a solder sucker or wick.

![Replacing pok3r PCB](/assets/images/keyboards/IMG_6453.png)
<figure><figcaption>Replacing old pok3r PCB (red) with new YD60MQ PCB (black)</figcaption></figure>

The PCB was replaced about a year after the board was first built, months after I started using QMK on my other boards (more on those in Part 2). The [custom keymap](https://github.com/ecliptik/qmk_firmware/blob/ecliptik/keyboards/yd60mq/keymaps/ecliptik/keymap.c) flashed on it is similar to the other boards I have, so combos and layers are consistent across all my boards.

## Final Product

![pok3r Final Form](/assets/images/keyboards/pok3r.jpg)
<figure><figcaption>pok3r Final Form</figcaption></figure>

With all these features checked off the list, the pok3r is is my daily driver for work and pleasure. It's a dream to type on with the tactility of the Holy Pandas, and the sound alone is worth the investment. Having the full power of QMK in the board greatly expands it's capabilities and gives me full ownership and pride in both the hardware and software aspects of it.

Granted it's borderline [Ship of Thesus](https://en.wikipedia.org/wiki/Ship_of_Theseus), with the only original parts the aluminum case and stabilizers, but that makes it a fully custom board that no one else has or could come close to replicating.
