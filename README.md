# Web DL API

Django RESTful api for Web DL.

## Installation

The Wel DL API requires the following software and OS to be installed:

- Apple Mac OS Yosemite 10.10.3+ or Microsoft Windows 10 Professional/Enterprise 64-bit
- [Docker Desktop](https://www.docker.com/products/docker-desktop) 

On lower versions of Mac OS, Windows, or on Linux, the [Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/) can also be installed, although the Web DL API is not originally developed using this tools.

### Runtime environment
- Docker 18.09.2+
- Docker Compose 1.23.2+

### Startup guide

 - Open a terminal window in the project folder.
 - Run the following code to prepare and start the required containers.

``` bash
$ make build && make start
```

### Update guide

 - Open a terminal window in the project folder.
 - Run the following code to update the containers.

``` bash
$ make stop && make clean
$ make update
```

### Shutdown guide

 - Open a terminal window in the project folder.
 - Run the following code to stop and remove the running containers.

``` bash
$ make stop && make clean
```

## Development

### Runtime environment
- Docker 18.09.2+
- Docker Compose 1.23.2+

### Create image

``` bash
$ docker build
```
or
``` bash
$ docker-compose build
```

### Microservices/containers

#### Start all project microservices/containers

``` bash
$ docker-compose up
```

#### Stop all project microservices/containers
``` bash
$ docker-compose down
```

#### Enter a container
``` bash
$ docker exec -it {container name or ID} bash
```
