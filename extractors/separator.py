import json
import requests


class CommentSeparator:
    def get_comments_text(comments):
        for comment in comments:
            yield{
                "cid": comment['cid'],
                "text": comment['text']
            }

    def get_author_image_file(url,author_name: str):
        response = requests.get(url)
        if response.status_code == 200:
            with open('./authors_images/'+author_name.replace("@","_")+".png", 'wb') as f:
                f.write(response.content)
            print("File downloaded successfully.")
        else:
            print("Failed to download file. Status code:", response.status_code)
