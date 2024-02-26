import json
import sys
import time
sys.path.insert(0, './')
from message_broker.consumers import MessageConsumers
from database.save_data import save_new_video_to_database





def main(ch, method, properties, body):
    json_body = json.loads(body)
    print("==========================================================")
    if method.routing_key == "save-new-data":
        # print(json_body['text_comments'])
        # print(json_body['comments_list'])

        # -- Insert into videos table
        save_new_video_to_database(json_body)
        # -- Insert into text_comments table
        # INSERT INTO text_comments(cid, video_id, text) VALUES('comment001', 'video123', 'This is so informative, thanks!');

        # -- Insert into comments_list table
        # INSERT INTO comments_list(cid, video_id, text, time, author, channel, votes, photo, heart) VALUES('comment100', 'video123', 'Great video!', '2023-06-15T12:34:56', 'Jane Doe', 'JaneDoeChannel', 250, 'https://example.com/photo.jpg', TRUE);









print("Listerning . . . . . .")
MessageConsumers.consume_messages(
    queue_name='database-queue', callback_function=main)



