FROM python:3.11.0-buster

# Setup labels
LABEL version = "1.0"
LABEL description = "Selenium docker container"
LABEL maintainer = "Rinesh Ramadhin"

RUN apt-get update

# Install Chromium
RUN apt-get install chromium -y

# Install Selenium dependencies
RUN apt-get install unzip xvfb libxi6 libgconf-2-4 default-jdk -y

# Install Chrome driver
WORKDIR /install
# Uncomment below for development on x64. e.g. Intel® Core™, AMD Ryzen™, etc.
#RUN wget -O chromedriver.zip https://github.com/electron/electron/releases/download/v12.2.3/chromedriver-v12.2.3-linux-x64.zip
# Uncomment below for development on arm64. e.g. Apple Silicon™.
# RUN wget -O chromedriver.zip https://github.com/electron/electron/releases/download/v12.2.3/chromedriver-v12.2.3-linux-arm64.zip
# Comment below temporarily during development when using an overwrite from above.
# Uncomment below for runtime on armv7. e.g. Raspberry Pi chipsets and similar.
RUN wget -O chromedriver.zip https://github.com/electron/electron/releases/download/v12.2.3/chromedriver-v12.2.3-linux-armv7l.zip
RUN unzip chromedriver.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

# Install Selenium
RUN wget -O selenium.jar https://selenium-release.storage.googleapis.com/3.9/selenium-server-standalone-3.9.1.jar
