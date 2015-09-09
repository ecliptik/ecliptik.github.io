---
layout: post
title: Automating Container Updates With Watchtower
categories: [containers]
tags: [docker, containers, watchtower]
---

You have your services containerized, you've just deployed them to your fleet for 100 container hosts and everything is running smoothly. Then you realize that you missed a crucial command in the [Dockerfile](https://docs.docker.com/reference/builder/), and well, re-building the container image and pushing to the repository is easy, but what about the 100's of containers out there running the old version?

There are a variety of tools to use in this situation, [Ansible](https://ansible.com), [Chef](https://www.chef.io/chef/), ssh and cronjobs, [Jenkins](https://jenkins-ci.org/), [Docker](https://www.docker.com/) itself, but stringing them all together and finding the right combination is tedious, time-consuming, and fragile. What you need it something to watch your running containers, check the Docker Registry for an updated container image, and then re-deploy the container with the exact same Docker run parameters.

That's where [Watchtower](https://labs.ctl.io/watchtower-automatic-updates-for-docker-containers/) comes in.

![Watchtower](/images/posts/watchtower.jpg)

## Simple Case Study

For a simple case study, two containers, one running [nginx](https://hub.docker.com/_/nginx/) and the other running [mongodb](https://hub.docker.com/_/mongo/) are configured. While the bulk of the configuration is complete, occasionally a container image update is needed. Right now these containers are running on a handful of systems, and re-deploying with an Ansible playbook is a good option without much overhead. But what happens on the next configuration change and the containers are running on 60 systems? 1000 systems? 10,000 systems? Ansible at this point may not be the right tool here.

Watchtower itself is a privledged container, with the ability to keep an eye on either all it's co-existing containers or only ones you specify. If you can already deploy containers onto your container host, deploying Watchtower should integrate easily into your existing container deployment workflow.

Starting up a Watchtower container and having it watch the containers nginx and mongodb is easy as running,

{% highlight bash %}
[root@containerhost-001 ~]# docker run -d \
>  --name watchtower \
>  -v /var/run/docker.sock:/var/run/docker.sock \
>  centurylink/watchtower nginx mongodb
{% endhighlight %}

This will pull the container from Docker Hub and run as a privileged container with access to the docker.sock via a mount,

{% highlight bash %}
[root@containerhost-001 ~]# docker ps -a | grep centurylink/watchtower
CONTAINER ID      IMAGE                         COMMAND                  CREATED          STATUS        PORTS    NAMES
2b794d39a65e      centurylink/watchtower        "/watchtower nginx m     11 seconds ago   Up 9 seconds            watchtower
{% endhighlight %}

Running a docker logs -f watchtower will show Watchtower checking every ~5 Minutes if the nginx and mongodb containers are updated on the Docker Registry,

{% highlight bash %}
[root@containerhost-001 ~]# docker logs -f watchtower
time="2015-09-08T23:10:08Z" level=info msg="Checking containers for updated images"
time="2015-09-08T23:10:08Z" level=info msg="Checking containers for updated images"
time="2015-09-08T23:15:11Z" level=info msg="Checking containers for updated images"
{% endhighlight %}

If the nginx container image is updated and pushed to the registyr, Watchtower will notice the update, [stop the container gracefully](https://labs.ctl.io/gracefully-stopping-docker-containers/), and restart the container using the updated image,

{% highlight bash %}
time="2015-09-08T23:36:11Z" level=info msg="Found new nginx;latest image (84b9c9eec0387b6fd3f41325acddde84f2fd2c1efea9b7c398826b71eeba8822)"
time="2015-09-08T23:36:12Z" level=info msg="Stopping /nginx (351486f71db2b658a176a594fc7408b0859a7998bdcd03d204c9654a81279c13) with SIGTERM"
time="2015-09-08T23:36:27Z" level=info msg="Starting /nginx"
{% endhighlight %}

## Conclusion
As you can see Watchtower is a powerful tool for keeping running containers up-to-date with what's in a Docker registry. The only thing Watchtower does not do (which is mentioned on their page) is the first-run issue, where Watchtower only has the ability to watch running containers up updates and not starting them initially.

There are a variety of Docker orchestration tools that can handle this ([Compose](https://docs.docker.com/compose/), [Swarm](https://docs.docker.com/swarm/), [Rancher](http://rancher.com/)) and maybe in the future Watchtower itself will gain a first-run feature.
