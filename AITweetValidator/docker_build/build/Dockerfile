FROM manifoldai/orbyter-ml-dev:1.7
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

COPY configs /configs

COPY data/model_eval /data/model_eval

COPY data/negative_processed /data/negative_processed

COPY data/processed /data/processed

COPY data/preprocessed /data/preprocessed

COPY src /src

COPY tweet_validator /tweet_validator

CMD ["/bin/sh", "run_scripts.sh"]