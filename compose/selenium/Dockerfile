FROM python:3.10.4-buster

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
#RUN wget -O chromedriver.zip https://github.com/electron/electron/releases/download/v12.2.2/chromedriver-v12.2.2-linux-x64.zip # For development on x64.
RUN wget -O chromedriver.zip https://github.com/electron/electron/releases/download/v12.2.2/chromedriver-v12.2.2-linux-armv7l.zip
RUN unzip chromedriver.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

# Install Selenium
RUN wget -O selenium.jar https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.0.0/selenium-server-4.0.0.jar
