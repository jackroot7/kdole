from threading import Thread
import pika
from pika.adapters.blocking_connection import BlockingChannel

class MessageConsumers:
    @classmethod
    def get_mq_channel(cls):
        #Declaring the credentials needed for connection like host, port, username, password, exchange etc
        credentials = pika.PlainCredentials("jackroot7","ega12345")
        connection= pika.BlockingConnection(pika.ConnectionParameters(host="172.17.20.249",port=5672, credentials= credentials))
        channel= connection.channel()
        return channel
    
    @classmethod
    def consume_messages(cls, queue_name: str, callback_function, exchanger_name:str = "youtube-exchange", ):
        channel: BlockingChannel = cls.get_mq_channel()
        channel.exchange_declare(exchanger_name, durable=True, exchange_type='topic')
        channel.basic_consume(queue=queue_name, on_message_callback=callback_function, auto_ack=True)
        Thread(target= channel.start_consuming()).start()
        
