# Web DL API

Django RESTful api for Web DL.

## Installation

The Wel DL API requires the following software and OS to be installed:

- Apple Mac OS Yosemite 10.10.3+ or Microsoft Windows 10 Professional/Enterprise 64-bit
- [Docker Desktop](https://www.docker.com/products/docker-desktop) 

On lower versions of Mac OS, Windows, or on Linux, the [Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/) can also be installed, although the Web DL API is not originally developed using this tools.

## Startup guide

 - Open a terminal window in the project folder.
 - Run the following code to prepare and start the required containers

``` bash
$ docker-compose up
```

## Development environment

### Docker
``` bash
Client: Docker Engine - Community
 Version:           18.09.2
 API version:       1.39
 Go version:        go1.10.8
 Git commit:        6247962
 Built:             Sun Feb 10 04:12:39 2019
 OS/Arch:           darwin/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          18.09.2
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.10.6
  Git commit:       6247962
  Built:            Sun Feb 10 04:13:06 2019
  OS/Arch:          linux/amd64
  Experimental:     false
```

### Docker-compose
``` bash
docker-compose version 1.23.2, build 1110ad01
docker-py version: 3.6.0
CPython version: 3.6.6
OpenSSL version: OpenSSL 1.1.0h  27 Mar 2018
```

## Create image

``` bash
docker build
```
or
``` bash
docker-compose build
```

## Microservices/containers

###  Start all project microservices/containers

``` bash
docker-compose up
```

### Stop all project microservices/containers
``` bash
docker-compose down
```

## Enter a container
``` bash
docker exec -it {container name or ID} bash
```