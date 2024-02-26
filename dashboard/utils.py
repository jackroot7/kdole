import sys
sys.path.insert(0, './')

from message_broker.producers import MessageProducers


class Utils:
    def submit_channel_id(channel_id):
        if not channel_id=="":
            MessageProducers.produce_message(queue_name='channel-queue', routing_key="video-extractor", message={"channel_id": channel_id})