---
layout: post
title: One Week With Mastodon
category: mastodon
tags: mastodon fediverse 100daystooffload
---
One week ago I posted [my first toot](https://fosstodon.org/@ecliptik/105585397423041642) on [Mastodon](https://joinmastodon.org) and I wanted to document my first weeks experience since it was much more eventful than I was expecting.

## Choosing an Instance

One of the first things you do when signing up for Mastodon is [choosing an instance](https://joinmastodon.org/communities). I didn't quite understand this at first, but eventually realized it was akin to choosing a Geocities neighborhood in the 90s. The instance you sign up for is like a community, with similar interests and themes that best fit your online identity and personality. After reading about different intances and browsing public timelines of users, I choose [Fosstodon](https://hub.fosstodon.org/about/) as my home instance. I was drawn to their focus on [Free and Open Source Software](https://en.wikipedia.org/wiki/Free_and_open-source_software), which fits my style of computing and online interests.

## Trying Things Out

The first few days I posted a few toots, followed some users on federated instances, and occasionally checked in on the local and federated timelines. I quickly realized that the federated timeline (a timeline which contains posts from all federated instances outside of Fosstodon) wasn't really for me, but the local timeline for Fosstodon was interesting. Because Fosstodon is only a few thousand users, there wasn't a firehose of posts to keep up on, and most users were posting links and comments on things that resonated with me.

I checking in on the local feed every few hours gave me some insight into what types of posts would add to the community and I started putting a few things out there just to test out the interface and gain confidence in using the service.

## Gemini and Gopherspace

The first topic that really caught my eye was I saw the hashtag `#gemini` trending on Fosstodon. I thought maybe it was related to space (which is sort of is), and after following the tag and reading toots from other users I discovered [Project Gemini](https://gemini.circumlunar.space). This in turn lead me to installing the [Lagrange](https://gmi.skyjake.fi/lagrange/) and [Bombadillo](https://bombadillo.colorfield.space) browsers. From there I started exploring all the sites I could find on `gemini://`, and eventually started browsing [Gopherspace](https://en.wikipedia.org/wiki/Gopher_%28protocol%29) (which is very much alive even in 2021). This re-kindled a curiosity of using networked computers that I haven't felt since using [Fidonet](https://en.wikipedia.org/wiki/FidoNet) and browsing my local BBS in the 90s.

## 512KB Club

The next trending hashtag I saw was `#512kbclub`, which is a challenge to [bring your personal websites homepage under 512KB](https://512kb.club). This site came in at 252KB without any tuning and I submitted it for inclusion and was added to the Blue team, just missing the Orange team cutoff. Looking at the sites size, much of it was Google Analytics, taking up around 138KB of the sites total size. I posted a [toot](https://fosstodon.org/web/statuses/105600821471040740) about joining the 512KB club and if there were any replacements for Google Analytics and recieved some helpful replies with alternatives. I replaced Google Analytics with [Goat Counter](https://www.goatcounter.com) and saw that the site was including `jquery` but not using it, that brought the site down to 24.7KB and into Green team (<100KB) territory.

## 100DaysToOffload

Another trending hastag was `#100daystooffload`, a challenge to [write 100 personal blog posts in one year](https://100daystooffload.com). This post is the first in what I hope will be many to participate in this challenge. I like the idea since it gives a goal to strive for and even if no one reads them it will provide personal growth experience.

## Bitwarden

About a year ago I started looking into alternative for LastPass as my password manager, as annual pricing had increased since I first started using it years ago and I knew there were better products out there. Inspired by seeing others on Fosstodon taking up tools and learning new things, I finally did the migration to [Bitwarden](https://bitwarden.com), which was a much easier process than I expected.

## ScreenShotSunday

It turns out on Sundays a thing to do on Fosstodon is post screenshots with the tag `#screenshotsunday`. Since I have a post on [screenshots through the years](https://www.ecliptik.com/Screenshots-Over-the-Years/) I tooted an old screenshot from [RedHat Linux 6.1 in 2000](https://fosstodon.org/@ecliptik/105611942604393139) and got a lot of positive responses, boosts, and followers leading to my highest "engagement".

## Summary

Much more happened than and I was expecting when I first thought about joining Mastodon last week. Because of the level of community and quality of posts, using Mastodon is much more rewarding than using Twitter where it feels overwhelming to keep up and posting is like shouting into a crowd of millions hoping a few will hear. I'm really looking forward to what will come with using Mastodon, and possibly other [Fediverse](https://fediverse.party), in the future.

The one critique I have of using Mastodon is interacting with other federated instances. When following users on other instances, the standard flow is to pop-up a seperate window and having to copy/paste your account in order to complete the action. I would expect since you're signed into an instance already that it would somhow automaticaly fill this in or just be more seamless overall. This may just be the way it works since they are federated, but it feels clunkier than it should.
