import json
import scrapetube

videos = scrapetube.get_search("Samia suluhu")

for video in videos:
    print(video['videoId'])
    json.dumps(video)