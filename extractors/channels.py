# trunk-ignore-all(black)
# UCqaVDGdr37sctTwNS3Lq_Uw : eGA
# UCBjbx3Y59dnH7UMnSCdSd-g : Ikulu Mawasiliano
import json
import sys
sys.path.insert(0, './')

from message_broker.consumers import MessageConsumers

sys.path.insert(0, './')
import scrapetube
from message_broker.producers import MessageProducers

class YouTubeChannel:
    """
    A class to represent a YouTube channel and fetch its videos.
    
    Attributes:
        channel_id (str): The ID of the YouTube channel.
    """
    def __init__(self, channel_id: str) -> None:
        """
        Initialize YouTubeChannel with the given channel_id.
        
        Args:
            channel_id (str): The ID of the YouTube channel.
        """
        self.channel_id = channel_id
    
    @classmethod
    def get_channel_videos(cls, channel_id: str):
        """
        Retrieve the list of videos for the given channel_id.
        
        Args:
            channel_id (str): The ID of the YouTube channel.
            
        Returns:
            list: A list of dictionaries representing video information.
        """
        channel_list = []
        for video in scrapetube.get_channel(channel_id, sleep=0):
            channel_list.append(video)
            
        return channel_list


    @classmethod
    def get_video_details(cls, channel_id: str):
        """
        Retrieve the list of videos for the given channel_id.
        
        Args:
            channel_id (str): The ID of the YouTube channel.
            
        Returns:
            list: A list of dictionaries representing video id and title.
        """
        channel_videos = cls.get_channel_videos(channel_id)
        channel_videos_list = []
        
        for video in channel_videos:            
            channel_videos_list.append({
                "id":video['videoId'],
                "title":video['title']['runs'][0]['text'],
                "length":video['lengthText']['simpleText'],
                "views":int(str(video['viewCountText']['simpleText']).removesuffix("views").replace(",","")) # Remove the word 'views' and "," to get th real number,
            })
        
        # Broadcast to RabitMQ 
        return MessageProducers.produce_message(queue_name='videos-queue', routing_key="comments-extractor", message={"channel_videos_list": channel_videos_list})
    
    @classmethod
    def main(cls, ch, method,properties,body):
        json_body = json.loads(body)
        YouTubeChannel.get_video_details(channel_id=json_body['channel_id'])

MessageConsumers.consume_messages(queue_name='channel-queue', callback_function=YouTubeChannel.main)