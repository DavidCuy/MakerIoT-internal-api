import pika
from api.config.queue import config

class BasicPikaClient:

    def __init__(self, driver='rabbitmq'):
        queue_config = config[driver]
        parameters = pika.URLParameters(queue_config['url'])

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

class BasicMessageSender(BasicPikaClient):

    def declare_queue(self, queue_name):
        print(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(queue=queue_name, durable=True)

    def send_message(self, exchange, routing_key, body):
        channel = self.connection.channel()
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body)
        print(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")

    def close(self):
        self.channel.close()
        self.connection.close()