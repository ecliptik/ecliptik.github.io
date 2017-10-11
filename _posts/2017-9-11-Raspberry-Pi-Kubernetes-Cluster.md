---
layout: post
title: Raspberry Pi Kubernetes Cluster
category: containers
tags: [docker, arm, kubernetes, raspberrypi]
---

Notes from setting up a three node [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) [Kubernetes](https://kubernetes.io) cluster using [HypriotOS 64-bit](https://github.com/DieterReuter/image-builder-rpi64/releases).

Originally from [Setup Kubernetes on a Raspberry Pi Cluster easily the official way!](https://blog.hypriot.com/post/setup-kubernetes-raspberry-pi-cluster/) with some additions to fix things I ran into when following the guide. This guide uses a 64-bit version of HypriotOS and only armv8 64-bit Docker images will work.

![RPI Cluster](/images/posts/k8s-rpi-cluster.jpg)

## Installing and Configuring HypriotOS
Flash [HypriotOS v1.6.0 64-bit](https://github.com/DieterReuter/image-builder-rpi64/releases) to SD card. By using HypriotOS we can avoid a lot of the issues that comes with installing Docker on ARM.

To begin, boot the Raspberry Pi to Hypriot, login and update system.

```shell
sudo apt update
sudo apt upgrade -y
```

## Installing Kubernetes
Install Kubernetes from [official package repositories](https://kubernetes.io/docs/setup/independent/install-kubeadm/#installing-kubelet-and-kubeadm) on each node.

```shell
sudo su -
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
apt update
apt install -y kubeadm kubelet
```

### Setup the Master Node
As root, init the cluster with the network CIDR for Flannel .

> As of this writing this will install and configure [Kubernetes 1.8](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG.md#v180)

```shell
kubeadm init --pod-network-cidr 10.244.0.0/16
```

As the `pirate` user setup kube config to run kube commands as non-root.

```shell
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
echo "export KUBECONFIG=${HOME}/.kube/config" >> ~/.bashrc
source ~/.bashrc
```

### Setup Flannel CNI
By default Kubernetes does not configure a [Container Network Interface](https://cncf.io/projects/) and needs to have one installed. [Flannel](https://github.com/coreos/flannel) has an arm64 version available and works reasonably well on the Raspberry Pi 3 and HypriotOS.

Install flannel using the arm64 image.

```shell
curl -sSL https://raw.githubusercontent.com/coreos/flannel/v0.9.0/Documentation/kube-flannel.yml | sed "s/amd64/arm64/g" | kubectl create -f -
```

## Setup Worker Nodes
On each worker node run the `kubeadm join` command that was output after successfully running `kubeadm init` on the master node.

Join the node to the cluster

```shell
sudo kubeadm join --token=$TOKEN
```

## Setup Iptables Rules

Add some additional iptables rules in order for external DNS and forwarding in containers to work properly. See this [issue](https://github.com/coreos/flannel/issues/799) for more information. Run these commands on the master and all worker nodes.

Install `iptables-persistent` package to save iptables rules,

```shell
sudo apt install -y iptables-persistent
```

Setup iptables for flannel CNI,

```shell
sudo iptables -P FORWARD ACCEPT
sudo iptables -t nat -A POSTROUTING -s 10.244.0.0/16 ! -d 10.244.0.0/16 -j MASQUERADE
sudo iptables -I FORWARD 1 -i cni0 -j ACCEPT -m comment --comment "flannel subnet"
sudo iptables -I FORWARD 1 -o cni0 -j ACCEPT -m comment --comment "flannel subnet"
```

Save iptable rules so they persist after reboot,

```shell
netfilter-persistent save
```

## Verifying
Show Node Status

```shell
$ kubectl get nodes -o wide
NAME      STATUS    ROLES     AGE       VERSION   EXTERNAL-IP   OS-IMAGE                       KERNEL-VERSION    CONTAINER-RUNTIME
navi      Ready     master    15m       v1.8.0    <none>        Debian GNU/Linux 9 (stretch)   4.9.13-bee42-v8   docker://Unknown
tael      Ready     <none>    9m        v1.8.0    <none>        Debian GNU/Linux 9 (stretch)   4.9.13-bee42-v8   docker://Unknown
tatl      Ready     <none>    8m        v1.8.0    <none>        Debian GNU/Linux 9 (stretch)   4.9.13-bee42-v8   docker://Unknown
```

Show Pod Status

```shell
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
