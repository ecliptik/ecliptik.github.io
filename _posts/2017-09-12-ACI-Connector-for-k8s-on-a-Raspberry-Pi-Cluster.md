---
layout: post
title: ACI Connector for k8s on a Raspberry Pi Cluster
description: Running the Azure Container Instances Connector for Kubernetes on a Raspberry Pi Cluster
category: containers
toc: true
tags: docker azure arm kubernetes raspberrypi
---

## Intro

Running the [Azure Container Instances Connector for Kubernetes](https://web.archive.org/web/20171104111735/https://github.com/azure/aci-connector-k8s) on a Raspberry Pi Cluster.

One of the most interesting features of [Azure Container Instances](https://docs.microsoft.com/en-us/azure/container-instances/) is the [Azure Container Instances Connector for Kubernetes](https://web.archive.org/web/20171104111735/https://github.com/azure/aci-connector-k8s). This adds an ACI "node" to an existing [Kubernetes](https://kubernetes.io) cluster and allows you to deploy pods to it. This "node" will run pods in ACI without having to create or manage and additional Azure VMs, just point-and-shoot a pod at it and it will run with no additional setup required.

By using the ACI Connector for Kubernetes on a Raspberry PI, a cluster can run homogenous ARM containers on-prem, but still have the ability to deploy and manage x86 containers to a cloud provider.

Read more about Azure Container Instances,
- [https://thenewstack.io/azure-container-instances-mean-cheaper-agile-container-tools-way/](https://thenewstack.io/azure-container-instances-mean-cheaper-agile-container-tools-way/)
- [https://docs.microsoft.com/en-us/azure/container-instances/](https://docs.microsoft.com/en-us/azure/container-instances/)
- [https://azure.microsoft.com/en-us/blog/announcing-azure-container-instances/](https://azure.microsoft.com/en-us/blog/announcing-azure-container-instances/)

## Creating an aci-connector-k8s ARM Image for Raspberry Pi
The upstream aci-connector-k8s image is x86 only, but since it's written in typescript it can easily be run on different architectures. To run on a Raspberry Pi k8s cluster, all that is required is building an armhf Docker image.

### Building a Nodejs ARM Docker Image

> Note: As of 9/12/2017 [Docker Hub Official Images support multi-platform](https://integratedcode.us/2017/09/13/dockerhub-official-images-go-multi-platform/) and re-building an image for armhf (or arm64, ppc64le, and s390x) is no longer required if using a supported image (currently Debian based only, Alpine based like below still need to be re-built).

The aci-connector-k8s [Dockerfile](https://web.archive.org/web/20211229050703/https://github.com/Azure/aci-connector-k8s/blob/master/Dockerfile) uses `node:8.4.0-alpine` as it's base image. While there are some "unofficial" node ARM images, lets create one from a somewhat official repository. This involves finding an armhf Alpine 3.6 image, copying/pasting the [node:8.4-alpine Dockerfile](https://github.com/nodejs/docker-node/blob/17c50cb300581280805a4183524fbf57840f3a7e/8.4/alpine/Dockerfile), replacing the `FROM` with the armhf version of alpine, and building the image.

There are two ways to build an armhf image,

- Build on Raspberry Pi
  - 100% native build, less likely to run into bugs
  - Painfully slow due to Raspberry Pi hardware
- Cross-build using [Docker for Mac](https://docs.docker.com/docker-for-mac/multi-arch/) or [Multiarch](https://github.com/multiarch)
  - Dramatically speed up builds
  - Could have unforseen issues due to running in an emulated environment

After first attempting option 1, two hours later and losing the ability to ssh into the Raspberry Pi, option 2 is a much faster approach. Building on a MacBook Pro using the built-in multiarch features of Docker for Mac works well, but is still slow even on a 4 core system. Fortunately Using up a 24-core [Packet.net](https://www.packet.net) Type 2 bare-metal instance to cross-compile using Multiarch is easy to do too.

> Note: The official Docker images for armhf are [arm32v6](https://hub.docker.com/r/arm32v6/) and [arm32v7](https://hub.docker.com/r/arm32v7/). These will work natively on a Raspberry Pi, Docker for Mac, Multiarch, and a Linux system with `qemu-*-static support`. For full details on these see [my post on cross-building Docker images](http://www.ecliptik.com/Cross-Building-and-Running-Multi-Arch-Docker-Images/).

A armhf multiarch nodejs [Dockerfile](https://github.com/ecliptik/dockerfiles/blob/master/node/Dockerfile.alpine.armhf) was built on the Packet.net Type 2 instance and pushed to Docker hub as `ecliptik/node:8.4.0-alpine-armhf`. This only took a few minutes using the Type 2 instance, much faster than Raspberry Pi or Macbook Pro.

Example Using Multiarch to re-build a node armhf alpine image,

```console
curl -sSL https://raw.githubusercontent.com/nodejs/docker-node/c044d61e6d02756bb8ed1557b2f0c7a0d7fead6f/8.4/alpine/Dockerfile | sed "s/alpine:3.6/multiarch\/alpine:armhf-v3.6/" > Dockerfile.node.armhf

docker build -f Dockerfile.node.armhf -t ecliptik/node:8.4.0-alpine-armhf .
docker push ecliptik/node:8.4.0-alpine-armhf
```

### Building an aci-connector-k8s ARM Docker Image
Once a nodejs arm-alpine image is created, clone the [aci-connector-k8s](https://web.archive.org/web/20171104111735/https://github.com/azure/aci-connector-k8s) repositoriy, and update the `Dockerfile` to use the `ecliptik/node:8.4.0-alpine-armhf` image. Additionaly, use the `Dockefile` below to use multi-stage builds for improved image size.

```dockerfile
### Base Image
# Setup up a base image to use in Build and Runtime images
FROM ecliptik/node:8.4.0-alpine-armhf AS base

WORKDIR /app
COPY package.json .

### Build Image
# Installs build dependencies and npm packages
# Creates artifacts to copy into Runtime image
FROM base AS build

# Install build OS packages
RUN set -ex && \
        buildDeps=' \
                make \
                gcc \
                g++ \
                python \
                py-pip \
                curl \
                openssl \
        ' && \
    apk add --no-cache \
       --virtual .build-deps $buildDeps

#Copy application into build image
COPY . .

# Install npm packages
RUN npm install -g
RUN npm install --silent --save-dev -g \
       gulp-cli \
       typescript

# Compile typescript sources to javascript artifacts
RUN tsc --target es5 connector.ts

### Runtime Image
# Copy artifacts from Build image and setups up entrypoint/cmd to run app
FROM base AS runtime

# Copy artifacts from Build Image
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/*.js ./
COPY --from=build /app/LICENSE ./

# Runtime command
ENTRYPOINT ["node"]
CMD ["connector.js"]
```

With an updated `Dockerfile` in the cloned repo, build the aci-connector-k8s image _on_ a Raspberry Pi,

```console
docker build -t ecliptik/aci-connector-k8s:alpine-armhf .
docker push ecliptik/aci-connector-k8s:alpine-armhf
```

> Note: Trying to build the image on non-native armhf platform like Docker for Mac or Multiarch may result in errors like `"SyntaxError: Unexpected end of JSON input"`. The image only seems to build on native Raspberry Pi or ARM hardware.

## Running the ACI Connector
Now that we have a armhf image capable of running on a Raspberry Pi, we can deploy the pod to a [Raspberry Pi Kubernetes cluster](http://www.ecliptik.com/Raspberry-Pi-Kubernetes-Cluster/).

First clone the [aci-connector-k8s](https://github.com/Azure/aci-connector-k8s) repository onto the Raspberry Pi cluster master,

```console
git clone https://github.com/Azure/aci-connector-k8s.git
```

Edit the `examples/aci-connector.yaml` and update the `image` to use the `ecliptik/aci-connector-k8s:alpine-armhf` image.

Next, if you used `kubeadm` to create your cluster and RBAC is enabled, you'll need to create a role and set it up for the connector. This is discussed in [this Github issue](https://github.com/Azure/aci-connector-k8s/issues/26#issuecomment-326809041) that includes creating a RBAC role and updating the service to use it.

Create the RBAC role for the connector,

```console
curl -sSL https://raw.githubusercontent.com/alexjmoore/aci-connector-k8s-arm/master/aci-connector-rbac.yaml | kubectl create -f -
```

Under `spec` in the `examples/aci-connector.yaml` add the RBAC role,

```console
serviceAccountName: aci-connector-sa
```

Finally after the connector is setup to use the armhf image and RBAC, follow the rest of the _Quickstart_ guide in the aci-connector-k8s [README](https://github.com/Azure/aci-connector-k8s/blob/master/README.md) to set up everything else required to run the connector (Azure keys, deployment of service, etc).

## Working Example

Updated `examples/aci-connector.yaml` with RBAC role and `ecliptik/aci-connector-k8s:alpine-armhf` image

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: aci-connector
  namespace: default
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: aci-connector
    spec:
      serviceAccountName: aci-connector-sa
      containers:
      - name: aci-connector
        image: ecliptik/aci-connector-k8s:alpine-armhf
        imagePullPolicy: Always
        env:
        - name: AZURE_CLIENT_ID
          value: 00000-000-00000-0000-0000
        - name: AZURE_CLIENT_KEY
          value: 00000-000-00000-0000-0000
        - name: AZURE_TENANT_ID
          value: 00000-000-00000-0000-0000
        - name: AZURE_SUBSCRIPTION_ID
          value: 100000-000-00000-0000-0000
        - name: ACI_RESOURCE_GROUP
          value: aci-test
```

Deploy the aci-connector pod,

```console
kubectl create -f examples/aci-connector.yaml
```

Wait a few minutes while the pod comes into service (mostly waiting for the image to pull) on a worker node.

Verify aci-connector pod has started,

```console
kubectl get pods
NAME                             READY     STATUS    RESTARTS   AGE
aci-connector-1252680567-b88w6   1/1       Running   0          3m
```

Verify aci-connector node is added,

```console
kubectl get nodes -o wide
NAME            STATUS    AGE       VERSION   EXTERNAL-IP   OS-IMAGE                        KERNEL-VERSION
aci-connector   Ready     2m        v1.6.6    <none>        <unknown>                       <unknown>
navi            Ready     1h        v1.7.5    <none>        Raspbian GNU/Linux 8 (jessie)   4.4.50-hypriotos-v7+
tael            Ready     1h        v1.7.5    <none>        Raspbian GNU/Linux 8 (jessie)   4.4.50-hypriotos-v7+
tatl            Ready     1h        v1.7.5    <none>        Raspbian GNU/Linux 8 (jessie)   4.4.50-hypriotos-v7+
```

Deploy `example/nginx-pod.yaml` pod from aci-connector-k8s repo,

```console
kubectl create -f examples/nginx-pod.yaml
pod "nginx" created
```

Verify pod deployed and is running in ACI,

```console
kubectl get pods -o wide
 NAME                             READY     STATUS    RESTARTS   AGE       IP               NODE
 aci-connector-1696751608-tcjcq   1/1       Running   0          24m       10.244.2.4       tael
 nginx                            1/1       Running   0          10s       104.42.235.280   aci-connector
```

## General Docker on ARM Links
While researching and setting this up I came across many good resources on running Docker on ARM,

- [https://help.packet.net/armv8/docker-on-armv8](https://help.packet.net/armv8/docker-on-armv8)
- [https://github.com/docker-library/official-images#architectures-other-than-amd64](https://github.com/docker-library/official-images#architectures-other-than-amd64)
- [https://blog.hypriot.com/post/first-touch-down-with-docker-for-mac/](https://blog.hypriot.com/post/first-touch-down-with-docker-for-mac/)
- [https://resin.io/blog/building-arm-containers-on-any-x86-machine-even-dockerhub/](https://resin.io/blog/building-arm-containers-on-any-x86-machine-even-dockerhub/)

ARM Docker Image Repositories
- [arm32v6](https://hub.docker.com/u/arm32v6/) - Works on RPI 3 with [HypriotOS](https://blog.hypriot.com/downloads/) 32-bit
- [arm32v7](https://hub.docker.com/u/arm32v7/) - Works on RPI 3 with [HypriotOS](https://blog.hypriot.com/downloads/) 32-bit
- [arm64v8](https://hub.docker.com/u/arm64v8/) - Currently no 64-bit version of HypriotOS, but will work on [Packet.net Type 2A Instances](https://www.packet.net/bare-metal/servers/type-2a/)
