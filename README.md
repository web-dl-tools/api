# Web DL API
![Web DL banner](.github/assets/banner.png)

![test workflow](https://github.com/web-dl-tools/api/actions/workflows/test.yml/badge.svg)

**Web DL API** is a Django RESTful api built to form the core of the entire Web DL stack.
It's the **sole requirement to run Web DL**.

### Some features
* Fully authenticated user creation and management.
* Secure, separate access to resources and files.
* Dynamic file download endpoint for secure file access management.
* Only stores files locally on device.
* Runs on less than 2 GB of memory across multiple containers.
* Authenticated websocket connection support for live status updates.
* Even more...

## Installation
The Wel DL API requires the following software and OS to be installed:

- Apple macOS Yosemite 10.10.3+ or Microsoft Windows 10 Professional/Enterprise 64-bit
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

On lower versions of macOS, Windows, or on Linux, the
[Docker Engine](https://hub.docker.com/search?offering=community&operating_system=linux&q=&type=edition)
can also be installed, although the Web DL API was not originally developed using this tool.

### Runtime environment
- Docker 18.09.2+
- Docker Compose 1.23.2+

### Startup guide
Prepare and start the required containers.
``` bash
$ make build && make start
```

### Update guide
Shutdown, update and restart the containers.
``` bash
$ make update && make start
```

### Shutdown and cleaning up guide
Stop, shutdown and remove the running containers and all images.
``` bash
$ make stop && make clean
```

## Development
For development the Web DL API requires the same stack to be installed as for installation.
No additional software is required.

### Create image(s)
``` bash
$ docker build
```
or
``` bash
$ docker-compose build
```

### Microservices/containers management

#### Start
Start all project microservices/containers
``` bash
$ docker-compose up
```

#### Stop
Stop all project microservices/containers
``` bash
$ docker-compose down
```

#### Enter
Enter a container
``` bash
$ docker exec -it {container name or ID} bash
```
