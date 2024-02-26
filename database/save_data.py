from config import cursor

def save_new_video_to_database(json_body):
    save_videosql = "INSERT INTO videos (id, title, length, views, likes) VALUES('{}','{}','{}','{}','{}') ON CONFLICT (id) DO NOTHING;".format(json_body['id'],json_body['title'],json_body['length'],json_body['views'],json_body['likes'])
    video_saved = cursor.execute(save_videosql)

    print("video_saved")
    print("comments_saved")
    print( json_body['comments_list'])
    for comment in json_body['comments_list']:
        print(comment)

        save_commentsql = "INSERT INTO comments_list(cid, video_id, text, time, author, channel, votes, photo, heart) VALUES('{}', '{}','{}', '{}', '{}', '{}', '{}', '{}', '{}')  ON CONFLICT (cid) DO NOTHING;".format(comment["cid"],json_body['id'],comment["text"],comment["time"],comment["author"],comment["channel"],comment["votes"],comment["photo"],comment["heart"])
        comments_saved = cursor.execute(save_commentsql)

    # save_videosql = "INSERT INTO videos (id, title, length, views, likes) VALUES('{}','{}','{}','{}','{}') ON CONFLICT (id) DO NOTHING;;".format(json_body['id'],json_body['title'],json_body['length'],json_body['views'],json_body['likes'])
    # video_saved = cursor.execute(save_videosql)
    
