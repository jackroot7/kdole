#producer
import json
import pika
from pika.adapters.blocking_connection import BlockingChannel

class MessageProducers:

    @classmethod
    def get_mq_channel(cls):
        #Declaring the credentials needed for connection like host, port, username, password, exchange etc
        credentials = pika.PlainCredentials("jackroot7","ega12345")
        connection= pika.BlockingConnection(pika.ConnectionParameters(host="172.17.20.249",port=5672, credentials= credentials))
        channel= connection.channel()
        return channel

    @classmethod
    def produce_message(cls, queue_name: str, routing_key: str,message: dict, exchanger_name:str = "youtube-exchange", ):

        channel: BlockingChannel = cls.get_mq_channel()

        print("Producing data to Queue . . . . . . .")
        print(routing_key)
        print(message)
        channel.exchange_declare(exchanger_name, durable=True, exchange_type="topic")
        channel.queue_declare(queue= queue_name)
        channel.queue_bind(exchange=exchanger_name, queue=queue_name, routing_key=routing_key)
        channel.basic_publish(exchange=exchanger_name, routing_key=routing_key, body= json.dumps(message))
        channel.close()
        
        return True


    