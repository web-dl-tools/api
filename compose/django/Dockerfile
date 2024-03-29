FROM rust:1.74.0-buster

# Setup labels
LABEL version = "2.0"
LABEL description = "Django docker container"
LABEL maintainer = "Rinesh Ramadhin"

# Setup environment arguments
ENV PYTHONUNBUFFERED 1
ARG POSTGRES_USER
ARG POSTGRES_DB

# Uninstall outdated python
RUN apt-get update
RUN apt-get remove --auto-remove python python3 -y
RUN apt-get purge python python3 -y

# Install Python
WORKDIR /install
RUN apt-get install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev \
libreadline-dev libffi-dev curl libbz2-dev git -y
RUN wget https://www.python.org/ftp/python/3.12.1/Python-3.12.1.tar.xz
RUN tar -xf Python-3.12.1.tar.xz

# Configure Python
WORKDIR /install/Python-3.12.1
RUN ./configure --enable-optimizations
RUN make install

# Install Python packages
WORKDIR /code
COPY requirements.txt .
RUN apt-get install python3-pip ffmpeg postgresql-client -y
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy application source
COPY . .

# Configure Git
RUN git config --system --add safe.directory /code

# Set starting configuration
ENTRYPOINT ["./compose/services-check.sh"]
