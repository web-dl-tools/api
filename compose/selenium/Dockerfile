FROM python:3.9-buster

# Setup labels
LABEL version = "1.0"
LABEL description = "Selenium docker container"
LABEL maintainer = "rinesh.ramadhin@gmail.com"

RUN apt-get update

# Install Chrome
RUN apt-get install chromium -y

# Install Selenium dependencies
RUN apt-get install unzip xvfb libxi6 libgconf-2-4 default-jdk -y

# Install Chrome driver
WORKDIR /install
#RUN wget -O chromedriver.zip https://github.com/electron/electron/releases/download/v12.0.7/chromedriver-v12.0.7-linux-x64.zip # For development on x64.
RUN wget -O chromedriver.zip https://github.com/electron/electron/releases/download/v12.0.7/chromedriver-v12.0.7-linux-armv7l.zip
RUN unzip chromedriver.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

# Install Selenium
RUN wget -O selenium-server-standalone.jar https://selenium-release.storage.googleapis.com/3.9/selenium-server-standalone-3.9.1.jar
