"""
This file is a consumer for the match event topic, the arguments for this script are the topics in which you will
receive messages.
"""
import pika
import sys

host = sys.argv[1]
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.exchange_declare(exchange='match', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[2:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
