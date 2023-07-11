
#!/usr/bin/env python
# coding=utf-8
import pika
credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(pika.ConnectionParameters('machine2',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='QueueAVS')
channel.basic_publish(exchange='', routing_key='QueueAVS', body='You got message 2')
connection.close()
