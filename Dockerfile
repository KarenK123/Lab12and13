############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Maintainer Karen

# Add the application resources URL

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip

# Copy the application folder inside the container
ADD /app /app

# Get pip to download and install requirements:
RUN pip install -r /app/requirement.txt

# Trying to install boto
RUN apt-get -y install python-boto
RUN pip install boto

# Run the access keys
RUN export AWS_ACCESS_KEY_ID=AKIAJBPNKK2PQQPPU7PA
RUN export AWS_SECRET_ACCESS_KEY=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

# Expose ports
EXPOSE 8888

# Set the default directory where CMD will execute
WORKDIR /app

# Set the default command to execute
# when creating a new container
# i.e. using CherryPy to serve the application
CMD python app.py
