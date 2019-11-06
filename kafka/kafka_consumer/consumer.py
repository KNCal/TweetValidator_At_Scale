from kafka import KafkaConsumer
import json
import os, stat


dir_path = 'preprocessed_data'
os.makedirs(dir_path)

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('user-texts',
                         group_id='group_1',
                         bootstrap_servers=['localhost:9092'],
                         # max_poll_records=10,
                         # fetch_max_bytes=2,
                         enable_auto_commit=True,
                         # key_deserializer=lambda item: json.loads(item.decode('utf-8')),
            			 value_deserializer=lambda item: json.loads(item.decode('utf-8')))
            			 # consumer_timeout_ms=100)

count=0
max_count = 10

while True:
    msg_pack = consumer.poll(timeout_ms=1000, max_poll_records=10)
    # msg_pack = consumer.poll(500)
    for tp, messages in msg_pack.items():
	    for message in messages:

			# Output to console 
		    print ("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
		                                          message.offset, message.key,
		                                          message.value))

		    dir_path_file = os.path.join(dir_path, message.key)
		    os.mknod(dir_path_file)
		    os.chmod(dir_path_file, stat.S_IWRITE)
		    os.chmod(dir_path_file, stat.S_IROTH)
		    with open(dir_path_file, 'w') as file:
                file.write(message.value) 

    count+=1
    if count > max_count:
    	files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
        	print(f)
    	
consumer.close()