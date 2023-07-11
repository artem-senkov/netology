#!/usr/bin/env python
# coding=utf-8
import pika
credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(pika.ConnectionParameters('machine1',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='QueueAVS')
def callback(ch, method, properties, body): print(" [x] Received %r" % body)
channel.basic_consume(queue='QueueAVS', on_message_callback=callback,auto_ack=False)
channel.start_consuming()
