# Web DL API
![Web DL banner](.github/assets/banner.png)

![test workflow](https://github.com/web-dl-tools/api/actions/workflows/test.yml/badge.svg)

**Web DL API** is a Django RESTful API built to form the core of the entire Web DL stack.
It's the **sole requirement to run Web DL**.

### Some features
* Fully authenticated with user creation and management.
* Secure, separate access to resources and files.
* Dynamic file download endpoint for secure file access management.
* Only stores files locally on device.
* Runs on less than 2 GB of memory across multiple containers.
* Authenticated websocket connection support for live status updates.
* Even more...

## Configuration
Configuration for the Web DL API is managed by an environment file. A base example is provided in the
repository as _.env.dist_. Please copy and rename this file to _.env_ and fill in the values.

| Property              | Description                                         | Required | Example                                               |
|-----------------------|-----------------------------------------------------|----------|-------------------------------------------------------|
| **USER_ID**           | The user ID of owner the files folder               | Yes      | 1                                                     |
| **FILES_PATH**        | The path of the files folder                        | Yes      | ./files                                               |
| **DJANGO_DEBUG**      | Enable/disable Django debug mode                    | Yes      | False                                                 |
| **DJANGO_SECRET_KEY** | Key used by Django to provide cryptographic signing | Yes      | someSecureDjangoSecretkeyFromhttps://djecrety.ir      |
| **SENTRY_DSN**        | The DSN URL for Sentry error tracking               | No       | https://1234567890abcdef@12345.ingest.sentry.io/67890 |
| **POSTGRES_USER**     | The PostgreSQL username                             | Yes      | postgres                                              |
| **POSTGRES_PASSWORD** | The PostgreSQL user password                        | Yes      | someSecurePW                                          |
| **POSTGRES_DB**       | The PostgreSQL default database                     | Yes      | postgres                                              |

## Installation
The Wel DL API requires the following software and OS to be installed:

- Operating System<sup>[1](#lower_os_versions)</sup>
    - Apple macOS Mojave 10.14 or higher (Intel chip)<sup>[2](#apple_silicon)</sup>
    - Microsoft Windows 10 Home/Pro 2004 (build 19041), Enterprise/Education 1909 (build 18363) or higher (64-bit)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

<a name="lower_os_versions">1</a>: On lower versions of macOS, Windows, or on Linux, the
[Docker Engine](https://hub.docker.com/search?offering=community&operating_system=linux&q=&type=edition)
can also be installed, although the Web DL Website was not originally developed using this tool.

<a name="apple_silicon">2</a>: Docker Desktop for Mac on Apple Silicon is available but requires a
[manual install of Rosetta 2](https://docs.docker.com/docker-for-mac/apple-silicon/#system-requirements).


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
