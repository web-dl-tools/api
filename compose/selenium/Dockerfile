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
#RUN wget https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip     # Enable for development on x64
RUN wget https://github.com/electron/electron/releases/download/v12.0.5/chromedriver-v12.0.5-linux-armv7l.zip
#RUN unzip chromedriver_linux64.zip     # Enable for development on x64
RUN unzip chromedriver-v12.0.5-linux-armv7l.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

# Install Selenium
RUN wget https://selenium-release.storage.googleapis.com/3.141/selenium-server-standalone-3.141.59.jar
