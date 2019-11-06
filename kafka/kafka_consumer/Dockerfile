FROM kimn/tweetvalidator_at_scale:1.0
ADD requirements_docker.txt /app/requirements_docker.txt

# set working directory to /app/
WORKDIR /app/

# set up pip and install python packages
RUN apt-get update &&\
pip3 install --upgrade pip &&\
pip3 install -r requirements_docker.txt

# create unprivileged user
RUN adduser --disabled-password --gecos ‘’ myuser

# make tweetvalidator available in Python path
ENV PYTHONPATH "${PYTHONPATH}:/app/src/"

COPY src /src

RUN ["python", "consumer.py"]