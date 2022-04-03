import pika

from server import settings


class RabbitClient:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='match', exchange_type='topic')
        self.response = None

    def publish_to_topic(self, routing_key: str, message: str) -> None:
        """ Sends a message to a topic on rabbitmq """
        self.channel.basic_publish(
            exchange='topic_logs', routing_key=routing_key, body=message)
