# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:buster

MAINTAINER HeyItsJono "https://github.com/heyitsjono"

# Set ALLOW_ORIGIN to '*' to accept all origins, or specify a comma-delimited list of origins e.g 'http://server.com,https://server.com'
ENV ALLOW_ORIGIN=

# Set ALLOW_CREDENTIALS to 'true' to allow credentials, defaults to false.
ENV ALLOW_CREDENTIALS=

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# WORKDIR sets the working directory (all following instructions operate within this directory);
WORKDIR /app

# Intall the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python Script
COPY . /app

# ENTRYPOINT configures the container to run as an executable; only the last ENTRYPOINT instruction executes
ENTRYPOINT ["python"]

# Suggest that user runs container with -p 5757:5000/tcp
EXPOSE 5757

# Trigger Python script
CMD ["pyCors.py"]