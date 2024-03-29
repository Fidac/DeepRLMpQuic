# Description of the Readme

The following Readme is taken from the original work that provided the implementation to run experiments. The Technical report pdf and the paper have a detailed explanation of the changes done to the original implementation. Also, the docker folder on this project is our adaptation to the original implementation and has all the changes. The way to run it is described in the Technical Report and can be supported by the original work documentation.

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
## Technical Report
The pdf file Appendix-Technical Report has a deep description an explanation not only in the changes to the original code to achieve our work, but also a description of the meaning and purpose of the other repositories that are used in this project and the original code.
