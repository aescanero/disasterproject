# disasterproject
Code examples for disaterproject blog (www.disaserproject.com)

## Core status

### Image: Debian 10

|------------------|--------|-----------------------------------|
| Element          | Status | Comments                          |
|------------------|--------|-----------------------------------|
| Virtual Machine  |[x] OK  | Download and deploy image         |
| Docker           |[x] OK  | Install and run                   |
| Docker-Compose   |[x] OK  | Install via Pip                   |
| Podman           |[x] OK  | Install and run                   |
| Kubernetes Core  |[x] OK  | Install and run                   |
| K3s              |[x] OK  | Install and run                   |
|------------------|--------|-----------------------------------|

### Image: CentOS 7

|------------------|------|-----------------------------------|
| Element          |Status| Comments                          |
|------------------|------|-----------------------------------|
| Virtual Machine  |[x] OK  | Download and deploy image         |
| Docker           |[x] OK  | Install and run                   |
| Docker-Compose   |[x] OK  | Install via YUM                   |
| Podman           |[x] OK  | Install and run                   |
| Kubernetes Core  |[x] OK  | Install and run                   |
| K3s              |[x] OK  | Install and run                   |
|------------------|--------|-----------------------------------|

### Image: Oracle Linux 8

|------------------|--------|-----------------------------------|
| Element          | Status | Comments                          |
|------------------|--------|-----------------------------------|
| Virtual Machine  |[x] OK  | Download and deploy image         |
| Docker           |[ ] FAIL| Need DockerEE                     |
| Docker-Compose   |[ ] FAIL| Need DockerEE                     |
| Podman           |[x] OK  | Install and run                   |
| Kubernetes Core  |[x] OK  | Install and run                   |
| K3s              |[ ]     | Not tested                        |
|------------------|--------|-----------------------------------|


## Storage status

### Kubernetes

|------------------|--------|-----------------------------------|
| Element          | Status | Comments                          |
|------------------|--------|-----------------------------------|
|                  |[ ]     |                                   |
|------------------|--------|-----------------------------------|

### K3s

|------------------|--------|-----------------------------------|
| Element          | Status | Comments                          |
|------------------|--------|-----------------------------------|
|                  |[ ]     |                                   |
|------------------|--------|-----------------------------------|


## Network status

### Kubernetes

|------------------|------------|------------------|-----------------------------------|
| Element          | Status     | Operating System | Comments                          |
|------------------|------------|------------------|-----------------------------------|
| Flannel          |[ ]         | Debian 10        |                                   |
| Flannel          |[ ]         | CentOS 7         |                                   |
| Flannel          |[ ]         | Oracle Linux 8   |                                   |
| Weave            |[ ]         | Debian 10        |                                   |
| Weave            |[ ]         | CentOS 7         |                                   |
| Weave            |[ ] FAIL    | Oracle Linux 8   |  Version 1.15 give ipvs problems  |
|------------------|------------|------------------|-----------------------------------|

### K3s

## Addons status

### Kubernetes

### K3s

## Tools and Clients status

### Kubernetes

### K3s

