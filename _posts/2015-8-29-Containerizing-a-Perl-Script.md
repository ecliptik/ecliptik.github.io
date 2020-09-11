---
layout: post
title: Containerizing a Perl Script
category: containers
tags: perl docker containers
---

Almost every IT department has one; a Perl script written decades ago by a long-gone employee that's critical to production. It does it's job well, but no one wants to touch or take responsibility for it. You just want to upgrade your infrastructure and bring it along, but there are so many [CPAN](http://www.cpan.org/) modules and inconsitencies you want never want to look at it again. What to do?

## Executable Containers

Most articles on containers focus on running a service, exposing ports and data volumes, but one feature frequently overlooked is the ability to run a container as an executable.

In [Docker](https://www.docker.com), the [ENTRYPOINT](https://docs.docker.com/reference/builder/#entrypoint) instruction makes this possible by running a command and accpeting command line arguments from `docker run`. Combining this with `-it` and `--rm` will run an interactive emphermal container, disappearing when the command is complete.

## Dockerfile

Let's walk through an example that runs a Perl script called [ps.pl](https://gist.github.com/ecliptik/9a868cbe348d87a5141a#file-ps-pl), which prints a simple process table using the CPAN module [Proc::ProcessTable](http://search.cpan.org/~durist/Proc-ProcessTable-0.39/ProcessTable.pm) and includes `-h` and `-v` arguments.

The following [Multi-Stage Dockerfile](https://docs.docker.com/develop/develop-images/multistage-build/) will build a container to run a simple perl script,

- Debian Stable Slim base image
- Install OS packages
- Install CPAN modules
- Copy [ps.pl](https://gist.github.com/ecliptik/9a868cbe348d87a5141a#file-ps-pl) script
- Set `ps.pl` script as [ENTRYPOINT](https://docs.docker.com/engine/reference/builder/#entrypoint)
- Set `-h` as default argument

Here is the [Dockerfile](https://gist.github.com/ecliptik/9a868cbe348d87a5141a#file-dockerfile) in full,

{% gist 9a868cbe348d87a5141a Dockerfile %}

## Dockerfile Breakdown

Standard start of a Dockerfile, using the [Official Debian image](https://hub.docker.com/_/debian/) tagged `stable-slim` as the `base` layer and a [label](https://docs.docker.com/engine/reference/builder/#label) for the image maintainer,

```dockerfile
FROM debian:stable-slim AS base
LABEL maintainer="Micheal Waltz <dockerfiles@ecliptik.com>"
```

Basic environment variables for Debian packages through `apt` non-interactive and set locale to UTF-8,

```dockerfile
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LC_ALL=C.UTF-8 \
    LANGUAGE=en_US.UTF-8
```

Install "runtime" packages for the `base` layer that other layers will inheriet. Sets `/app` as [WORKDIR](https://docs.docker.com/engine/reference/builder/#workdir),

```dockerfile
# Install runtime packages
RUN apt-get update \
    && apt-get install -y \
      perl

# Set app dir
WORKDIR /app
```

Intermediate `build` layer which is used temporarily to install packages and modules that won't be used directly at runtime. Using an intermeiate layer will save space in the resulting image and no include packages that aren't used explicitly for runtime operation, improving security posture.


```dockerfile
# Intermediate build layer
FROM base AS build
#Update system and install packages
RUN apt-get update \
    && apt-get install -yq \
        build-essential \
        cpanminus
```

Install Perl [CPAN](https://www.cpan.org/) packages and dependencies with [cpanminus](http://search.cpan.org/~miyagawa/App-cpanminus-0.05/cpanm) which works well within a container build environment,

```dockerfile
# Install cpan modules
RUN cpanm Proc::ProcessTable Data::Dumper
```

Create final `run` layer for the resulting image and copy `/usr/local` from the intermediate `build` layer to include required CPAN modules,

```dockerfile
# Runtime layer
FROM base AS run

# Copy build artifacts from build layer
COPY --from=build /usr/local /usr/local
```

Copy [ps.pl](https://gist.github.com/ecliptik/9a868cbe348d87a5141a#file-ps-pl) script into `WORKDIR` (aka `/app`) of the container. This is put near the end of the `Dockerfile` since it is the file most likely to change and will allow re-using of cache for previous layers, [speeding up subsequent builds](https://thenewstack.io/understanding-the-docker-cache-for-faster-builds/).

```dockerfile
# Copy perl script
COPY ./ps.pl .
```


Set `ENTRYPOINT` to the [ps.pl](https://gist.github.com/ecliptik/9a868cbe348d87a5141a#file-ps-pl) script,

```dockerfile
# Set entrypoint
ENTRYPOINT [ "/app/ps.pl" ]
```

## Running the Containerized Perl Script

Now that the Dockerfile is complete, build a container image with the name `ps-perl`,

```console
🚀➜ docker build -t ps-perl .
```

With a container image ready, run it with `docker run -it --rm ps-perl`, using the `-it` and `--rm` options so the container is removed when it exits,,

```console
🚀➜ docker run -it --rm ps-perl
PID    TTY        STAT     START                    COMMAND
1      /dev/pts/0 run      Fri Sep 11 17:45:16 2020 /usr/bin/perl -w /app/ps.pl
--------------------------------
uid:  0
gid:  0
pid:  1
fname:  ps.pl
ppid:  0
pgrp:  1
sess:  1
ttynum:  34816
flags:  4210944
minflt:  1684
cminflt:  0
majflt:  0
cmajflt:  0
utime:  40000
stime:  10000
cutime:  0
cstime:  0
priority:  20
start:  1599846316
size:  12779520
rss:  8192000
wchan:  0
time:  50000
ctime:  0
state:  run
euid:  0
suid:  0
fuid:  0
egid:  0
sgid:  0
fgid:  0
pctcpu:    5.00
pctmem:  0.07
cmndline:  /usr/bin/perl -w /app/ps.pl
exec:  /usr/bin/perl
cwd:  /app
cmdline:  ARRAY(0x55fb475bb9f0)
environ:  ARRAY(0x55fb472dd500)
tracer:  0
```

## Command Line Arguments

Command line arguments will also pass into the container when run using the [CMD](https://docs.docker.com/engine/reference/builder/#cmd) to pass to `ENTRYPOINT`,

`-h`

```console
🚀➜ docker run -it --rm ps-perl -h
A simple perl version of ps
```

`-v`

```console
🚀➜ docker run -it --rm ps-perl -v
Version: 1.0
```

## Conclusions

By using the `-slim` variant of Debian for the base image and multi-stage builds, the resulting container size is just over 130MB. Using a smaller image like [Alpine Linux](https://hub.docker.com/_/alpine/) could further reduce the image size, but could introduce [known caveats](http://gliderlabs.viewdocs.io/docker-alpine/caveats/) because of [musl libc and glibc differences](https://wiki.musl-libc.org/functional-differences-from-glibc.html).

```console
🚀➜ docker images
ps-perl             latest              938c3dde86d7        29 minutes ago      134MB
```

## Additional References

- [Dockerising a Perl application](http://robn.io/docker-perl/)
- [Downsizing Docker Containers](https://intercityup.com/blog/downsizing-docker-containers.html)
- [Proc::ProcessTable Example](http://search.cpan.org/~durist/Proc-ProcessTable-0.39/ProcessTable.pm)

(Updated 9/11/2020)
