---
layout: post
title: Emulating ARM64 on Linux
categories: [operatingsystems]
tags: [operatingsystems, arm64, ubuntu]
---

Over the last few years I've [championed](https://www.google.com/search?q=micheal+waltz+arm64) the ultra-low-power and high density of a [64-bit](ttp://www.arm.com/products/processors/armv8-architecture.ph) ARM platform in the datacenter. The promise of thousands of cores all sipping power and taking up less room than the equivalent Intel architecture to me is both exciting and practical as a large systems IT engineer.

Combining with the simplicity of a [microservices architecture](http://microservices.io/) with the advantages of [immutable infrastructure](http://chadfowler.com/blog/2013/06/23/immutable-deployments/) running across a sea-of-[containers](https://www.docker.com) and you have an extremely powerful agile development and operations platform.

Working for a [semiconductor company](https://www.qualcomm.com/) specializing in [ARM Architecture](https://en.wikipedia.org/wiki/ARM_architecture) unfortuantely does not guarentee me access to this exciting new tech ([yet](http://www.extremetech.com/computing/194701-qualcomm-will-enter-arm-server-market-with-major-partners-broad-solutions)), but through the wonders of emulation bringing up a development environment is just a few commands away.

The following gist contains the steps on standing up a emulated ARM64 virtual machine either with [Ubuntu](http://www.ubuntu.com/) or [Debian](http://www.ubuntu.com/) operating system. This should be enough for anyone wanting to tinker with an ARM64 before getting their hands on real hardware.

The biggest downside of this approach is while you can assign as much memory to QEMU as the host system has available, it is bound to only one CPU, which combined with the emulation environment leads to extremely slow performancen on CPU intensive tasks.

{% gist 81ad7484d522097dca7f %}
