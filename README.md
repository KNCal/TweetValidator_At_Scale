# TweetValidator_At_Scale

## Purpose

The purpose of this project is to demonstrate processing data and building machine learning models at scale.

For this purpose, it uses an AI tool (AI-Tweet-Validator) to process a dataset of over 1200 users' 1000-tweets to build a model for each user to identify fraudulent tweets.

Since a model is built for each user based on his/her/their tweets, the amount of processing and space required is fairly large, and as the number of users increase, a scaleable solution is necessary.


## The Architecture

This project uses the following architecture:





### The Objects

- Tweet texts file per user 
- S3 store input and output files
- AWS lambda
- Docker container pods, each hosting ML/AI application and a consumer wrapper
- EKS cluster to orchestrate scaling of kafka, zookeeper, docker pods
- kafka/zookeeper cluster
- Dashboard Flask application


### The Flow

A file of tweet texts per user is uploaded on S3, which triggers a producer lambda function, sending a file as a message to a kakfa topic.

Kafka/zookeeper manage topic queues.

EKS manages the scaling of the kafka (the queue), and consumers (docker pods).

Processing is done inside dockers and output to S3, where it is accessed by the dashboard.


### Extension to pipeline 

Output from dockers or S3 can be sent back into kafka queue as a new topic for further computations using statefulsets.







For this use case, and many others, the pipeline is able to implement a machine-learning/AI application (provided it is written and best practices are followed for scaleability).



