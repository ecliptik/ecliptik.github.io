---
layout: post
title: Containerizing a Perl Script
category: containers
tags: perl docker containers
---

Almost every IT department has one; a Perl script written over a decade ago by a long-gone employee. It does it's job well, but no one wants to touch or take responsibility for it. You just want to upgrade your infrastructure and bring it along, but there are so many [CPAN](http://www.cpan.org/) modules and inconsitencies you want never want to look at it again. What to do?

## Executable Containers

Most articles on containers focus on running a service, exposing ports and data volumes, but one feature frequently overlooked is the ability to run a container as an executable.

In [Docker](https://www.docker.com), the [ENTRYPOINT](https://docs.docker.com/reference/builder/#entrypoint) instruction makes this possible by running a command and accpeting command line arguments from *docker run*. Combining this with *-it* and *--rm* will run an interactive emphermal container, disappearing when the command is complete.

## Dockerfile Example

Let's walk through an example that runs a simple perl script called [ps.pl](https://gist.github.com/ecliptik/9a868cbe348d87a5141a#file-ps-pl), which prints a simple process table using the CPAN module [Proc::ProcessTable](http://search.cpan.org/~durist/Proc-ProcessTable-0.39/ProcessTable.pm) and has simple *-h* and *-v* arguments.

This [Dockerfile](https://gist.github.com/ecliptik/9a868cbe348d87a5141a#file-dockerfile) will setup the following environment,

- Ubuntu 14.04 LTS
- Install required Ubuntu packages
- Install required CPAN modules
- Copy ps.pl script
- Set ps.pl script as **ENTRYPOINT**

---

```dockerfile
FROM ubuntu:14.04
MAINTAINER Micheal Waltz <ecliptik@gmail.com>
```

This is a standard start to a Dockerfile, using the Docker Hub [Ubuntu image](https://hub.docker.com/_/ubuntu/) tagged 14.04 and the name of the maintainer.

---

```dockerfile
ENV DEBIAN_FRONTEND=noninteractive LANG=en_US.UTF-8 LC_ALL=C.UTF-8 LANGUAGE=en_US.UTF-8
```

Here some environment variables are set, which make installing Debian packages through *apt* completely non-interactive and make the environment fully UTF-8.

---

```dockerfile
RUN [ "apt-get", "-q", "update" ]
RUN [ "apt-get", "-qy", "--force-yes", "upgrade" ]
RUN [ "apt-get", "-qy", "--force-yes", "dist-upgrade" ]
RUN [ "apt-get", "install", "-qy", "--force-yes", \
      "perl", \
      "build-essential", \
      "cpanminus" ]
RUN [ "apt-get", "clean" ]
RUN [ "rm", "-rf", "/var/lib/apt/lists/*", "/tmp/*", "/var/tmp/*" ]
```

Fully updates Ubuntu, installs **perl** and **cpanminus** packages, and cleans up apt to save some space.

---

```dockerfile
RUN ["cpanm", "Proc::ProcessTable", "Data::Dumper" ]
```

Uses [cpanminus](http://search.cpan.org/~miyagawa/App-cpanminus-0.05/cpanm) which makes installing CPAN modules dead simple within a Docker container to install dependencies.

---

```dockerfile
COPY [ "./ps.pl", "/app/ps.pl" ]
RUN [ "chmod", "+x",  "/app/ps.pl" ]
```

Copies *ps.pl* script into /app of the container and makes it executable.

---

```dockerfile
ENTRYPOINT [ "/app/ps.pl" ]
```

Sets the ENTRYPOINT to the *ps.pl* script.

## Running the Perl Script From a Container

Now that the Dockerfile is complete, build a container image with the name **ps-perl**,

```console
% docker build -t ps-perl .
```

With a container image ready, run it using the *-it* and *--rm* options so the container is automatically removed when completd,

```console
% docker run -it --rm ps-perl
PID    TTY        STAT     START                    COMMAND
1      /dev/console run      Sun Aug 30 04:39:38 2015 /usr/bin/perl -w /app/ps.pl
--------------------------------
uid:  0
gid:  0
pid:  1
fname:  ps.pl
...
pctmem:  0.08
cmndline:  /usr/bin/perl -w /app/ps.pl
exec:  /usr/bin/perl
cwd:  /
```

Command line arguments will also pass into the container when run,

*-h*

```console
% docker run -it --rm ps-perl -h
A simple perl version of ps
```

*-v*

```console
% docker run -it --rm ps-perl -v
Version: 1.0
```

## Conclusions

The major downside to this approach is Ubuntu containers usually run over 300MB in size, which is a bit overkill, but taken in the context of portability, ease of setup, and sharability amongst other Docker containers, it's worth it.

When working with more complicated CPAN modules ([Net::SSH](http://search.cpan.org/dist/Net-SSH/SSH.pm)), there could be additional dependencies within the OS before the module will build properly. Tracking these down can take some additional time, but once everything is put together in the container you won't have to worry about it ever again.

Using a base container image other than Ubuntu, such as [Alpine](https://hub.docker.com/_/perl/), may also yield a smaller container footprint, but could use up a lot of time getting all the dependencies right on a more complicated script.

### Additional References

- [Dockerising a Perl application](http://robn.io/docker-perl/)
- [Downsizing Docker Containers](https://intercityup.com/blog/downsizing-docker-containers.html)
- [Proc::ProcessTable Example](http://search.cpan.org/~durist/Proc-ProcessTable-0.39/ProcessTable.pm)
