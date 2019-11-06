
import json
import boto3
import logging
from kafka import KafkaProducer
import urllib
import ssl

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

context = ssl.create_default_context()
context.options &= ssl.OP_NO_TLSv1
context.options &= ssl.OP_NO_TLSv1_1

ip_address = '172.20.98.198:9092'
# ip_address = 'kafka1:9092,kafka2:9092,kafka3:9092'

producer = KafkaProducer(
   bootstrap_servers=[ip_address],
   linger_ms=10)



def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))

    bucket = record['s3'][0]['bucket']['name']
    # make sure key is set to tweets folder in trigger
    key = record['s3'][0]['object']['key']
    logger.info('Reading {} from {}'.format(key, bucket))

    s3_clientobj = s3.get_object(Bucket=bucket, Key=key)
    s3_clientdata = s3_clientobj['Body'].read()

    try:
        future = producer.send('user-texts', key=key, value=s3_clientdata.encode('utf-8'))
        record_metadata = future.get(timeout=10)
        logger.info("sent event to Kafka! topic {} partition {} offset {} json,dumps {}".format(record_metadata.topic, record_metadata.partition, record_metadata.offset), json.dumps(record).encode('utf-8'))
        producer.flush()

    except Exception as e:
        logger.info(e)
        logger.info('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e



        