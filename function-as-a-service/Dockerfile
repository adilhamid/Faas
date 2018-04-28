FROM python:2.7

# Create the group and user to be used in this container
RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask

RUN apt-get update;apt-get install -y openssh-server vim

# Create the working directory (and set it as the working directory)
RUN mkdir -p /home/flask/function-as-a-service/web
WORKDIR /home/flask/function-as-a-service/web

# Install the package dependencies (this step is separated
# from copying all the source code to avoid having to
# re-install all python packages defined in requirements.txt
# whenever any source code change is made)
COPY requirements.txt /home/flask/function-as-a-service/web
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . /home/flask/function-as-a-service/web

RUN chown -R flask:flaskgroup /home/flask

USER flask