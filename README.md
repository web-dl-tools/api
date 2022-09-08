# Web DL API
![Web DL banner](.github/assets/banner.png)

![test workflow](https://github.com/web-dl-tools/api/actions/workflows/test.yml/badge.svg)

**Web DL API** is a Django RESTful API build to form the core of the entire Web DL stack.
It's the **sole requirement to run Web DL**.

### Some features
* Fully authenticated with user creation and management.
* Secure, separate access to resources and files.
* Dynamic file download endpoint for secure file access management.
* Only stores files locally on device.
* Runs on less than 2 GB of memory across multiple containers.
* Authenticated websocket connection support for live status updates.
* Even more...

## Quick start

```bash
$ git clone https://github.com/web-dl-tools/api.git
$ cd ./api
// Fill in .env file
$ make start
```

Please review the [requirements](https://web-dl-tools.github.io/docs/#/requirements), [installation](https://web-dl-tools.github.io/docs/#/installation) and [configuration](https://web-dl-tools.github.io/docs/#/configuration) steps in [the documentation](https://web-dl-tools.github.io/docs/) for additional information and troubleshooting.
