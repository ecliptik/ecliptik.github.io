---
layout: post
title: Building a website with Github and Jekyll
categories: [github, coding]
tags: [docker, jekyll, github]
---

After a long time of [www.ecliptik.com](http://www.ecliptik.com) being offline I finally brought it back online with [Github Pages](https://pages.github.com/). I really like the concept of having a static site using Markdown files and a template to quickly bring online a modern looking blog without the hassle of configuring a content management system, web server, or database.

While building the site, I created a [Dockerfile](https://github.com/ecliptik/ecliptik.github.io/blob/master/Dockerfile) to make viewing the site locally before pushing to Github. The container image [ecliptik/jekyll](https://hub.docker.com/r/ecliptik/jekyll/) built from this Dockerfile is also on Docker Hub.

```shell
jezebel in ~/git/ecliptik.github.io (master●●)
% docker run -it --rm -p 4000:4000 -v $(pwd):/app ecliptik/jekyll:latest
Configuration file: /app/_config.yml
            Source: /app
       Destination: /app/_site
      Generating...
                    done.
 Auto-regeneration: enabled for '/app'
Configuration file: /app/_config.yml
    Server address: http://0.0.0.0:4000/
  Server running... press ctrl-c to stop.
      Regenerating: 1 file(s) changed at 2015-08-22 05:19:34 ...done in 0.108220049 seconds.
      Regenerating: 1 file(s) changed at 2015-08-22 05:19:34 ...done in 0.116449572 seconds.
```
