---
layout: post
title: Raspberry Pi Kubernetes Cluster
description: Setting up a Kubernetes on a cluster of RaspberryPis
category: containers
toc: true
tags: docker arm kubernetes raspberrypi
---

## Intro

Notes from setting up a three node [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) [Kubernetes](https://kubernetes.io) cluster using [HypriotOS 64-bit](https://github.com/DieterReuter/image-builder-rpi64/releases).

Originally from [Setup Kubernetes on a Raspberry Pi Cluster easily the official way!](https://blog.hypriot.com/post/setup-kubernetes-raspberry-pi-cluster/) with some additions to fix things I ran into when following the guide. This guide uses a 64-bit version of HypriotOS and only armv8 64-bit Docker images will work.

[![RPI Cluster](/assets/images/posts/k8s-rpi-cluster.jpg){:width="50%" }](/assets/images/posts/k8s-rpi-cluster.jpg)

## Installing and Configuring HypriotOS
Flash [HypriotOS 64-bit](https://github.com/DieterReuter/image-builder-rpi64/releases) to SD card. By using HypriotOS we can avoid a lot of the issues that comes with installing Docker on ARM.

> You can skip the following steps for updating, setting up the k8s repo, and installing the k8s package using `--userdata` with the [flash](https://github.com/hypriot/flash) tool. See this [example](https://github.com/ecliptik/rpi/blob/master/hypriot/user-data.yml).

To begin, boot the Raspberry Pi to Hypriot, login and update system,

```console
sudo apt update
sudo apt upgrade -y
```

## Installing Kubernetes
Install Kubernetes from [official package repositories](https://kubernetes.io/docs/setup/independent/install-kubeadm/#installing-kubelet-and-kubeadm) on each node,

```console
sudo su -
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
apt update
apt install -y kubeadm kubelet
```

### Setup the Master Node
As root, init the cluster with the network CIDR for Flannel,

> As of this writing this will install and configure [Kubernetes 1.8](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG.md#v180)

```console
kubeadm init --pod-network-cidr 10.244.0.0/16
```

As the `pirate` user setup kube config to run kubectl commands as non-root,

```console
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
echo "export KUBECONFIG=${HOME}/.kube/config" >> ~/.bashrc
source ~/.bashrc
```

### Setup Flannel CNI
By default Kubernetes does not configure a [Container Network Interface](https://cncf.io/projects/) and needs to have one installed. [Flannel](https://github.com/coreos/flannel) has an arm64 version available and works reasonably well on the Raspberry Pi 3 and HypriotOS.

Install flannel using arm64 images,

> With older versions of flannel, additinoal iptables rules were required, this was fixed in [v0.9.1](https://github.com/coreos/flannel/pull/872) (thanks for the tip Frank!)

```console
curl -sSL https://raw.githubusercontent.com/coreos/flannel/v0.9.1/Documentation/kube-flannel.yml | sed "s/amd64/arm64/g" | kubectl create -f -
```

## Setup Worker Nodes
On each worker node run the `kubeadm join` command that was output after successfully running `kubeadm init` on the master node.

Join the node to the cluster,

```console
sudo kubeadm join --token=$TOKEN
```

## Verifying
Show Node Status,

```console
$ kubectl get nodes -o wide
NAME      STATUS    ROLES     AGE       VERSION   EXTERNAL-IP   OS-IMAGE                       KERNEL-VERSION        CONTAINER-RUNTIME
navi      Ready     master    13m       v1.8.4    <none>        Debian GNU/Linux 9 (stretch)   4.9.65-hypriotos-v8   docker://17.10.0-ce
tael      Ready     <none>    4m        v1.8.4    <none>        Debian GNU/Linux 9 (stretch)   4.9.65-hypriotos-v8   docker://17.10.0-ce
tatl      Ready     <none>    4m        v1.8.4    <none>        Debian GNU/Linux 9 (stretch)   4.9.65-hypriotos-v8   docker://17.10.0-ce
```

Show Pod Status,

```console
$ kubectl get pods --all-namespaces
NAMESPACE     NAME                           READY     STATUS    RESTARTS   AGE
kube-system   etcd-navi                      1/1       Running   0          15m
kube-system   kube-apiserver-navi            1/1       Running   0          15m
kube-system   kube-controller-manager-navi   1/1       Running   1          15m
kube-system   kube-dns-596cf7c484-qrqsx      3/3       Running   0          14m
kube-system   kube-flannel-ds-2rzg7          1/1       Running   0          8m
kube-system   kube-flannel-ds-852gj          1/1       Running   0          13m
kube-system   kube-flannel-ds-qxmws          1/1       Running   0          10m
kube-system   kube-proxy-92762               1/1       Running   0          10m
kube-system   kube-proxy-r78jd               1/1       Running   0          14m
kube-system   kube-proxy-tfdjr               1/1       Running   0          8m
kube-system   kube-scheduler-navi            1/1       Running   0          15
```

## Run A Test Pod

Using [Docker Hub Official Multi-Platform Images](https://integratedcode.us/2017/09/13/dockerhub-official-images-go-multi-platform/) makes running official Docker hub images on arm64 hardware much easier. Since Docker Hub now understands architecture manifest, no specific architecture tags are required and any official images will work on a Raspberry Pi k8s cluster without a specific tag.

> Official images based off Alpine Linux currently do not work - see [Issue #304](https://github.com/gliderlabs/docker-alpine/issues/304) for more information.

In this example, we'll run the [official nginx image](https://hub.docker.com/_/nginx/) and have it listen on port 80.

First, deploy a nginx service with 3 replicas,

```console
$ kubectl run nginx --image=nginx --replicas=3 --port=80
deployment "nginx" created
```

Expose pods in nginx service on port 80,
```console
$ kubectl expose deployment nginx --port 80
service "nginx" exposed
```

Get endpoints for nginx service,

```console
$ kubectl get endpoints
NAME         ENDPOINTS                                   AGE
kubernetes   192.168.7.220:6443                          37m
nginx        10.244.1.2:80,10.244.1.3:80,10.244.2.2:80   23s
```

Run curl against an endpoint IP to test,

> `curl` should work against all endpoint IPs on all nodes

```console
$ curl 10.244.2.2 | head -n 5
<DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
```
