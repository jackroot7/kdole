import json
import sys
import time
sys.path.insert(0, './')


from message_broker.consumers import MessageConsumers
from message_broker.producers import MessageProducers
from video_comments import YouTubeComments







def main(ch, method,properties,body):
    json_body = json.loads(body)
    print("==========================================================")
    print(json_body)

    for video_link in json_body["channel_videos_list"]:
        video_data = YouTubeComments.main('https://www.youtube.com/watch?v='+str(video_link['id']))
        completed_video_data = {
            'id': video_link['id'], 
            'title': video_link['title'], 
            'length': video_link['length'], 
            'views': int(video_link['views']),
            'likes': int(video_data['likes']),
            'text_comments': video_data['text_comments'],
            'comments_list': video_data['comments_list'],
        }

        if len(completed_video_data['text_comments']) > 0:
            MessageProducers.produce_message(queue_name='sentiment-queue', routing_key="sentiment-analysor", message={"vid": video_link['id'], "video_comments": completed_video_data['text_comments']})
        
        MessageProducers.produce_message(queue_name='database-queue', routing_key="save-new-data", message=completed_video_data)


print("Listerning . . . . . .")
MessageConsumers.consume_messages(queue_name='videos-queue', callback_function=main)



