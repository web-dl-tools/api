FROM python:3.10.6-buster

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
# Uncomment below for development on x64. e.g. Intel® Core™ i7, AMD Ryzen™ 9, etc.
#RUN wget -O chromedriver.zip https://github.com/electron/electron/releases/download/v12.2.3/chromedriver-v12.2.3-linux-x64.zip
# Uncomment below for development on arm64. e.g. Apple Silicon M1 Pro.
# RUN #wget -O chromedriver.zip https://github.com/electron/electron/releases/download/v12.2.3/chromedriver-v12.2.3-linux-arm64.zip
# Comment below temporarily during development when using an overwrite from above.
# This is the armv7 runtime compatible with most Raspberry Pi chipsets and similar.
RUN wget -O chromedriver.zip https://github.com/electron/electron/releases/download/v12.2.3/chromedriver-v12.2.3-linux-armv7l.zip
RUN unzip chromedriver.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

# Install Selenium
RUN wget -O selenium.jar https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.0.0/selenium-server-4.0.0.jar
