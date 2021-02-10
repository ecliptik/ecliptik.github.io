---
layout: post
title: Launching a Gemini Capsule
category: gemini
tags: gemini smallweb 100daystooffload
---

## Gemawhat?

Even since I started [using Mastodon](https://www.ecliptik.com/One-Week-With-Mastodon/) a couple of weeks ago, [Project Gemini](https://gemini.circumlunar.space) is one of the most exciting new technologies I've come across in the last few years.

I won't go into full detail on what Gemini is, but similar to [why I made a Gopherhole](https://www.ecliptik.com/Making-a-Gopherhole-and-Phlog/), Gemini is a newer Internet protocol that strips away the bloat of the modern web to a core set of concepts, generality, and maximum power-to-weight-ratio.

> Gemini is a new, collaboratively designed internet protocol, which explores the space in between gopher and the web, striving to address (perceived) limitations of one while avoiding the (undeniable) pitfalls of the other.

While setting up a Gopherhole was fun and a throwback to an era long gone, Gemini has modern features but still sticks to simplicity,

* Encryption by default
* Gemtext similar to Markdown
* MIME type support
* Support for multiple protocols; `gemini://`, `gopher://`, `http://`

## Creating a Capsule

Creating a Gemini Capsule was a much lower barrier than it seems, since it's `Gemtext` is very similar to Markdown and can almost convert 1:1 (with the exception of in-line links). So posts written in Markdown for a static blog (like [Jekyll](https://www.jekyllnow.com)) can easily work in Gemini. The tool [md2gemini](https://github.com/makeworld-the-better-one/md2gemini) makes this even more seamless by converting Markdown specific things to Gemtext.

With having content ready to go, hosting is the next challenge. Bringing up your own Gemini server is easy enough, with a [large number of Gemini servers](https://github.com/kr1sp1n/awesome-gemini#servers) available. I just went with using my Pubnix account at [rawtext.club](https://rawtext.club) which provides a `public_gemini` option. This is also where [my gopherhole](gopher://rawtext.club:70/1~ecliptik) is hosted.

## Creating a Toolset

Manually converting markdown posts, using `scp` to copy them to RTC, and putting together some basic `index.gmi` and `blog.gmi` files, and I had a live [gemini capsule](gemini://rawtext.club/~ecliptik/) and running. This was nice, but I wanted to publish posts on this blog to both Gopherspace and Geminispace together and needed something that would have some additional features,

* Convert Jekyll markdown to Gopher and Gemtext
* Create a 10 most recent posts page and an archive page of all posts
* Add tags to posts, group posts by tags, and have all tags listed on the archive page
* Basic header/footer support
* Build a [gemfeed](https://tildegit.org/solderpunk/gemfeed) to syndicate in Geminispace

Iterating on the [tools I wrote for gopher](https://www.ecliptik.com/Making-a-Gopherhole-and-Phlog/) by including using `md2gemini` to convert to `Gemtext` got me partially there, but was still missing some more features. After more iterations, I had [updatesmallweb.sh](https://github.com/ecliptik/ecliptik.github.io/blob/master/_scripts/updatesmallweb.sh) that converts Jekyll posts to gopher and gemini. Now whenever I publish a post on Jekyll, I can run this script to convert the post to Gopher and Gemini. Doing `git push` to github, then `git pull` on RTC and everything is up-to-date.

Here's the script in action building the gopherhole and capsule,

```bash
micheal in git/ecliptik.github.io/_scripts on  master [$!?] took 2s
🚀➜ ./updatesmallweb.sh -t all
Converting post ../_posts/2011-01-22-Vim-rdesktop-external-monitors-and-X-Forwarding-on-a-Google-CR-48.md to gopher
Converting post ../_posts/2015-08-20-Building-a-website-with-Github-and-Jekyll.md to gopher
Converting post ../_posts/2015-08-21-Decompiling-Interactive-Fiction.md to gopher
Converting post ../_posts/2015-08-28-Emulating-ARM64-on-Linux.md to gopher
Converting post ../_posts/2015-08-29-Containerizing-a-Perl-Script.md to gopher
Converting post ../_posts/2015-09-08-Automating-Container-Updates-With-Watchtower.md to gopher
Converting post ../_posts/2017-09-11-Raspberry-Pi-Kubernetes-Cluster.md to gopher
Converting post ../_posts/2017-09-12-ACI-Connector-for-k8s-on-a-Raspberry-Pi-Cluster.md to gopher
Converting post ../_posts/2017-10-02-Cross-Building-and-Running-Multi-Arch-Docker-Images.md to gopher
Converting post ../_posts/2021-01-26-One-Week-With-Mastodon.md to gopher
Converting post ../_posts/2021-01-31-Making-a-Gopherhole-and-Phlog.md to gopher
Converting post ../_posts/2021-02-09-Launching-a-Gemini-Capsule.md to gopher
Creating gophermap: ../_gopher/_posts/gophermap
Converting post ../_posts/2011-01-22-Vim-rdesktop-external-monitors-and-X-Forwarding-on-a-Google-CR-48.md to gemini
Creating tag page ../_gemini/_tags/vim.gmi
Creating tag page ../_gemini/_tags/google.gmi
Creating tag page ../_gemini/_tags/cr-48.gmi
Creating tag page ../_gemini/_tags/linux.gmi
Creating tag page ../_gemini/_tags/blogger.gmi
Converting post ../_posts/2015-08-20-Building-a-website-with-Github-and-Jekyll.md to gemini
Creating tag page ../_gemini/_tags/docker.gmi
Creating tag page ../_gemini/_tags/jekyll.gmi
Creating tag page ../_gemini/_tags/github.gmi
Converting post ../_posts/2015-08-21-Decompiling-Interactive-Fiction.md to gemini
Creating tag page ../_gemini/_tags/zmachine.gmi
Creating tag page ../_gemini/_tags/interactivefiction.gmi
Creating tag page ../_gemini/_tags/zork.gmi
Converting post ../_posts/2015-08-28-Emulating-ARM64-on-Linux.md to gemini
Creating tag page ../_gemini/_tags/operatingsystems.gmi
Creating tag page ../_gemini/_tags/arm.gmi
Creating tag page ../_gemini/_tags/ubuntu.gmi
Converting post ../_posts/2015-08-29-Containerizing-a-Perl-Script.md to gemini
Creating tag page ../_gemini/_tags/perl.gmi
Creating tag page ../_gemini/_tags/containers.gmi
Converting post ../_posts/2015-09-08-Automating-Container-Updates-With-Watchtower.md to gemini
Creating tag page ../_gemini/_tags/watchtower.gmi
Converting post ../_posts/2017-09-11-Raspberry-Pi-Kubernetes-Cluster.md to gemini
Creating tag page ../_gemini/_tags/kubernetes.gmi
Creating tag page ../_gemini/_tags/raspberrypi.gmi
Converting post ../_posts/2017-09-12-ACI-Connector-for-k8s-on-a-Raspberry-Pi-Cluster.md to gemini
Creating tag page ../_gemini/_tags/azure.gmi
Converting post ../_posts/2017-10-02-Cross-Building-and-Running-Multi-Arch-Docker-Images.md to gemini
Converting post ../_posts/2021-01-26-One-Week-With-Mastodon.md to gemini
Creating tag page ../_gemini/_tags/mastodon.gmi
Creating tag page ../_gemini/_tags/fediverse.gmi
Creating tag page ../_gemini/_tags/100daystooffload.gmi
Converting post ../_posts/2021-01-31-Making-a-Gopherhole-and-Phlog.md to gemini
Creating tag page ../_gemini/_tags/gopher.gmi
Converting post ../_posts/2021-02-09-Launching-a-Gemini-Capsule.md to gemini
Creating tag page ../_gemini/_tags/gemini.gmi
Creating tag page ../_gemini/_tags/smallweb.gmi
Creating gemlog index: ../_gemini/gemlog.gmi
Creating archive index: ../_gemini/_posts/index.gmi
Creating tag index page: ../_gemini/_tags/index.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/100daystooffload.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/arm.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/azure.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/blogger.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/containers.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/cr-48.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/docker.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/fediverse.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/gemini.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/github.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/google.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/gopher.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/index.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/interactivefiction.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/jekyll.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/kubernetes.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/linux.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/mastodon.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/operatingsystems.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/perl.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/raspberrypi.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/smallweb.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/ubuntu.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/vim.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/watchtower.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/zmachine.gmi
Adding tag link gemini://rawtext.club/~ecliptik/_tags/zork.gmi
Generating feed "Gemlog Archive", which should be served from gemini://rawtext.club/~ecliptik/_posts/feed.xml
Adding 2021-02-09-Launching-a-Gemini-Capsule.gmi with title 'Launching a Gemini Capsule'...
Adding 2021-01-31-Making-a-Gopherhole-and-Phlog.gmi with title 'Making a Gopherhole and Phlog'...
Adding 2021-01-26-One-Week-With-Mastodon.gmi with title 'One Week With Mastodon'...
Adding 2017-10-02-Cross-Building-and-Running-Multi-Arch-Docker-Images.gmi with title 'Cross Building and Running Multi-Arch Docker Images'...
Adding 2017-09-12-ACI-Connector-for-k8s-on-a-Raspberry-Pi-Cluster.gmi with title 'ACI Connector for k8s on a Raspberry Pi Cluster'...
Adding 2017-09-11-Raspberry-Pi-Kubernetes-Cluster.gmi with title 'Raspberry Pi Kubernetes Cluster'...
Adding 2015-09-08-Automating-Container-Updates-With-Watchtower.gmi with title 'Automating Container Updates With Watchtower'...
Adding 2015-08-29-Containerizing-a-Perl-Script.gmi with title 'Containerizing a Perl Script'...
Adding 2015-08-28-Emulating-ARM64-on-Linux.gmi with title 'Emulating ARM64 on Linux'...
Adding 2015-08-21-Decompiling-Interactive-Fiction.gmi with title 'Decompiling Interactive Fiction'...
Wrote Atom feed to ../_gemini/_posts/feed.xml.
```

![Gemlog in Lagrange](/assets/images/posts/gemlog-in-lagrange.png)
<figure><figcaption>Gemlog in Lagrange</figcaption></figure>

## What's Next

Now that I have a better understanding of how Gopher and Gemini work, and have some tooling to make things seamless between gopher/gemini/web my plans are to improve `updatesmallweb.sh` so it's almost a static site generator. Some of the documentation and examples needs updating as well, so others can use it, and already [gemini://gemini.lottalinuxlinks.com](gemini://gemini.lottalinuxlinks.com) has.

Gemini is one of those things that you either really like or don't quite understand it. I'm in the former group, as it reminds me of what the Internet was before it turned into what it is today. The phrase "Eternal August" is one that comes to mind, as it's specification is not meant to really be improved upon and should remain the same for the foreseeable future. This allows creativity to flourish in a restricted environment, like the Demo Scene or modern homebrew Gameboy Games.

For more on exploring Geminispace, see [awesome-gemini](https://github.com/kr1sp1n/awesome-gemini).
