---
layout: post
title: Decompiling Interactive Fiction
categories: [coding]
tags: [zmachine, interactivefiction, zork]
---

A couple of weeks ago a friend of mine pointed me to the web-based interactive fiction piece called [Aisle](http://iplayif.com/?story=http://parchment.toolness.com/if-archive/games/zcode/Aisle.z5.js). As I played it, I immediately started wondering how I could get a text blob of all the possible paths instead of trying to figure out all the actions required to input into the interpreter.

<img src="{{ site.baseurl }}/images/aisle.png" alt="Aisle Introduction"/>

## Finding the Source
I took a look at the source and discovered Aisle was using a tool called [Parchment](https://github.com/curiousdannii/parchment), which is designed for interactive web fiction. Looking at the javascript source of Aisle, it is basically a [http://parchment.toolness.com/if-archive/games/zcode/Aisle.z5.js](base64 text blob) in a javascript function passed to Parchment.

Since Linux has a [base64\(1\)](http://man7.org/linux/man-pages/man1/base64.1.html) utility, I figured I'd strip out the javascript and decode the text to see if I could read the text blob and thus read every possible scenario in the story.

{% highlight bash %}
% sed -e "s/processBase64Zcode('//g" Aisle.z5.js \
| sed -e "s/');//g" \
| base64 --decode > Aisle.z5
{% endhighlight %}

At first I did this without output redirection, and it flooded my terminal with binary control characters, essentially frying it. I killed the tmux window, and started again, this time looking to see if the file type was known.

{% highlight bash %}
% file Aisle.z5
Aisle.z5: Infocom (Z-machine 5, Release 1 / Serial 990528)
{% endhighlight %}

A quick search on Infocom and [Z-Machine](https://en.wikipedia.org/wiki/Z-machine), shows that Z-Machine was developed for interactive fiction in 1979 for Infocom text adventure games, of which Zork was the first and where the Z comes from. There's a whole lot of interesting [history](http://inform7.com/if/interpreters/) online about Z-Machine if anyone wants to know more (spoiler: it's related to [UCSD Pascal](https://en.wikipedia.org/wiki/UCSD_Pascal) P-Machine).

## Decoding Z-Machine

Now that the raw source was available, the next step was actually finding useful text. A search found an open source tool called [Frotz](http://frotz.sourceforge.net/) that can play these files, and the next thing I know I have Aisle running in a terminal and it works just like it does in the browser.

Some addition searches didn't really uncover much on how to *de-compile* a Z-Machine file. Nothing in the Debian repos, and some additional man pages for Frotz didn't lead to much.

Finally I found [Z-Code Tools](http://inform-fiction.org/zmachine/zcode.html). There was no compiled binaries for Linux, and if there were, they probably don't work anymore on a newer version of Linux. I downloaded the source and a make later made the binaries magically appear. The freshly compiled **txd** tool finally yielded the results I wanted:

{% highlight bash %}
% ./txd /var/tmp/Aisle.z5 | grep gnocchi | head -5
gnocchiyou
S139: "You pick up a bag of gnocchi and turn it over. The doughy balls weigh your eyes; gnocchi, women, a woman, statues, a slow motion crash of flesh on show her some gnocchi and then you eat it and live happily ever after." intelligent. Leaving the gnocchi you walk over and drop to a knee. "Will you
{% endhighlight %}

I put the full text dump of Aisle into a [gist](https://gist.github.com/ecliptik/1ce9c21f04c984c705b9) if anyone is interested in taking a look.

There are many other tools included in ztools that can provide additional information, such as listing a dictionary of available actions and commands.

## Final Thoughts

Interactive fiction is just more than a big blob of text. Since the early days of Z-Machine, these stories have not only included fascinating stories, but also puzzles and other methods of fully immersing a reader. Fully exploring and creating Z-Machine and Interactive fiction is best left to to the [experts](http://inform7.com/learn/) if you'd like to learn more.

It also appears the Z-code Tools are not packaged in [Debian](http://www.debian.org), and this may be a fun project to do sometime.

*\#zmachine \#interactivefiction \#zork*
