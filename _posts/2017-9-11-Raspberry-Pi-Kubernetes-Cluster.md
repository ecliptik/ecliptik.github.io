---
layout: post
title: Raspberry Pi Kubernetes Cluster
category: containers
tags: [docker, arm, kubernetes, raspberrypi]
---

Notes from setting up a three node [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) [Kubernetes](https://kubernetes.io) cluster using [HypriotOS](https://github.com/hypriot/image-builder-rpi/releases).

Originally from [Setup Kubernetes on a Raspberry Pi Cluster easily the official way!](https://blog.hypriot.com/post/setup-kubernetes-raspberry-pi-cluster/) with some additions to fix things I ran into when following the guide.

![RPI Cluster](/images/posts/k8s-rpi-cluster.jpg)

## Installing and Configuring HypriotOS
Flash HypriotOS v1.5.0 to SD card. By using HypriotOS we can avoid a lot of the issues that comes with installing Docker on ARM.

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

Create a cluster service account which makes some things work better (not entirey if this is required, but it doesn't hurt).

```shell
kubectl create clusterrolebinding permissive-binding \
        --clusterrole=cluster-admin \
        --user=admin \
        --user=kubelet \
        --group=system:serviceaccounts
```

### Setup Flannel CNI
By default Kubernetes does not configure a [Container Network Interface](https://cncf.io/projects/) and needs to have one installed. [Flannel](https://github.com/coreos/flannel) has an ARM version available and works reasonably well on the Raspberry Pi 3.

> Note: As of this writing, v0.8.0 has a [known bug](https://github.com/coreos/flannel/issues/773) where it will not start on an ARM architecture. Using v0.7.1 is recommended.

Setup RBAC role for flannel since newer versions of k8s have this enabled by default.

```shell
curl -sSL https://rawgit.com/coreos/flannel/v0.7.1/Documentation/kube-flannel-rbac.yml | kubectl create -f -
```

Install flannel using the ARM image.

```shell
curl -sSL https://rawgit.com/coreos/flannel/v0.7.1/Documentation/kube-flannel.yml | sed "s/amd64/arm/g" | kubectl create -f -
```

Add some additional iptables rules in order for external DNS and forwarding in containers to work properly. See this [issue](https://github.com/coreos/flannel/issues/799) for more information.

Install `iptables-persistent` package to save iptables rules,

```shell
apt install -y iptables-persistent
```

```shell
sudo iptables -P FORWARD ACCEPT
sudo iptables -t nat -A POSTROUTING -s 10.244.0.0/16 ! -d 10.244.0.0/16 -j MASQUERADE
sudo iptables -I FORWARD 1 -i cni0 -j ACCEPT -m comment --comment "flannel subnet"
sudo iptables -I FORWARD 1 -o cni0 -j ACCEPT -m comment --comment "flannel subnet"
```

Save iptable rules,

```shell
netfilter-persistent save
```

## Setup Worker Nodes
On each worker node run the `kubeadm join` command that was output after successfully running `kubeadm init` on the master node.

Join the node to the cluster

```shell
sudo kubeadm join --token=$TOKEN
```


Add some additional iptables rules in order for external DNS and forwarding in containers to work properly. See this [issue](https://github.com/coreos/flannel/issues/799) for more information.

Install `iptables-persistent` package to save iptables rules,

```shell
apt install -y iptables-persistent
```

```shell
sudo iptables -P FORWARD ACCEPT
sudo iptables -t nat -A POSTROUTING -s 10.244.0.0/16 ! -d 10.244.0.0/16 -j MASQUERADE
sudo iptables -I FORWARD 1 -i cni0 -j ACCEPT -m comment --comment "flannel subnet"
sudo iptables -I FORWARD 1 -o cni0 -j ACCEPT -m comment --comment "flannel subnet"
```

## Verifying
Show Node Status

```shell
$ kubectl get nodes -o wide
NAME      STATUS    AGE       VERSION   EXTERNAL-IP   OS-IMAGE                        KERNEL-VERSION
navi      Ready     18m       v1.7.5    <none>        Raspbian GNU/Linux 8 (jessie)   4.4.50-hypriotos-v7+
tael      Ready     11m       v1.7.5    <none>        Raspbian GNU/Linux 8 (jessie)   4.4.50-hypriotos-v7+
tatl      Ready     11m       v1.7.5    <none>        Raspbian GNU/Linux 8 (jessie)   4.4.50-hypriotos-v7+
```

Show Pod Status

```shell
$ kubectl get pods --all-namespaces
NAMESPACE     NAME                           READY     STATUS    RESTARTS   AGE
kube-system   etcd-navi                      1/1       Running   0          7m
kube-system   kube-apiserver-navi            1/1       Running   0          7m
kube-system   kube-controller-manager-navi   1/1       Running   0          7m
kube-system   kube-dns-2459497834-g4tz6      3/3       Running   0          6m
kube-system   kube-flannel-ds-vlnw5          2/2       Running   0          57s
kube-system   kube-flannel-ds-xsfnc          2/2       Running   0          4m
kube-system   kube-flannel-ds-zntxs          2/2       Running   0          48s
kube-system   kube-proxy-b17qz               1/1       Running   0          48s
kube-system   kube-proxy-m105w               1/1       Running   0          6m
kube-system   kube-proxy-wpjj4               1/1       Running   0          57s
kube-system   kube-scheduler-navi            1/1       Running   0          7m
```
