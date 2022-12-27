# Multi-Path Scheduling with Deep Reinforcement Learning
This project contains my master thesis and all the files for reproducing
the results.

## Repositories
This work is split in several public repositories:

 * [Multi-path scheduling with deep reinforcement learning](https://bitbucket.org/marcmolla/multi-path-scheduling-with-deep-reinforcement-learning/):
 this repository. Includes the thesis, the offline RL agent, pre-compiled binaries and the testing scripts. Also, a docker
 image is available for the tests.
 * [GoRL](https://bitbucket.org/marcmolla/gorl/): Open implementation of an agent in Go, as is described in the thesis.
 * [MP-QUIC](https://github.com/marcmolla/mp-quic): Fork of the multi-path QUIC implementation that includes the RL agent
 

## Installation
Follow this instructions for installing all the testing framework of this thesis.

### Ubuntu and Docker

Download the last ubuntu server LTS (18.04 at this moment) and create a new VM on virtual box with the
image. The main characteristics that I used are: 2 vCPU, 2048 MB of RAM and 20 GB of storage.

Once Ubuntu is installed, install docker: 

```$ sudo snap install docker```

---
***Note***

These instructions are tested in an iMac with OSX 10.13.6 using virtual box for running the VM. If you find any issue
please open an [issue.](https://bitbucket.org/marcmolla/multi-path-scheduling-with-deep-reinforcement-learning/issues?status=new&status=open)

---
***Note***

Please follow the instructions detailed in https://github.com/docker/docker-snap/issues/1 for avoiding errors with 
running docker from non-root user.
---

### Install MP-QUIC

MP-QUIC is a client/server implementation of a multi-path QUIC written in Go. To install it, first install Go:
```
$ sudo snap install go
```
and check the Go version installed:
```
$ go version
go version go1.10.3 linux/amd64
```

Before the installation, we have to manually install the GoRL repository:
```
$ mkdir $HOME/go
$ cd $HOME/go
$ mkdir -p src/bitbucket.com/marcmolla/
$ cd bitbucket.com/marcmolla/
$ git clone https://bitbucket.com/marcmolla/gorl

```
and the HDF5 lib:
```
sudo apt install libhdf5-dev
```

The MP-QUIC project is a fork of a fork, so first you have to install the original project:
```
~$ cd go/
~/go$ go get github.com/lucas-clemente/quic-go
```
And after that, configure the remote pointing to our MP-QUIC repository and get all dependencies:
```
$ cd ~/go/src/github.com/lucas-clemente/quic-go
$ git remote add mp-quic https://github.com/marcmolla/mp-quic
$ git fetch mp-quic
$ git checkout master_thesis
$ go get -t -u ./...
```

Last command is going to fail, due to an update in the mint library (check original 
[MP-QUIC](https://multipath-quic.org/2017/12/09/artifacts-available.html) repository). For solving the problem:
```
cd ~/go/src/github.com/bifurcation/mint
$ git reset --hard a6080d464fb57a9330c2124ffb62f3c233e3400e
$ cd ~/go/src/github.com/lucas-clemente/quic-go
$ go build
```
And finally
```
$ go install ./...
```
With this, all the MP-QUIC executables should be at `$HOME/go/bin`

## Docker image

Clone this repository into you VM:
```
$ git clone https://marcmolla@bitbucket.org/marcmolla/multi-path-scheduling-with-deep-reinforcement-learning.git
```

and copy the mp-quic client and server:
```
$ cp ~/go/bin/client_benchmarker ~/multi-path-scheduling-with-deep-reinforcement-learning/docker/quic/client_mt
$ cp ~/go/bin/example ~/multi-path-scheduling-with-deep-reinforcement-learning/docker/quic/server_mt
```
and the certificates
```
$ cp ~/go/src/github.com/lucas-clemente/quic-go/example/*.pem ~/multi-path-scheduling-with-deep-reinforcement-learning/docker/quic/
```

Now, you can generate the docker image by typing:
```
$ cd ~/multi-path-scheduling-with-deep-reinforcement-learning/docker
$ docker build -t mpscheduling .
```

For running the docker image, type:
```
$ docker run --privileged=true --cap-add=ALL -v /lib/modules:/lib/modules -p 8888:8888 -it --add-host quic.clemente.io:10.0.0.20 mpscheduling
