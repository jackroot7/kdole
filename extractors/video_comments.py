import sys
import json
import re
import time
import requests
from separator import CommentSeparator



YOUTUBE_COMMENTS_AJAX_URL = 'https://www.youtube.com/comment_service_ajax'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
# csv file name
FILE_NAME = 'ytb_comments.csv'

# set parameters
# filter comments by popularity or recent, 0:False, 1:True
SORT_BY_POPULAR = 1
# default recent
SORT_BY_RECENT = 1
# set comment limit
COMMENT_LIMIT = 100

YT_CFG_RE = r'ytcfg\.set\s*\(\s*({.+?})\s*\)\s*;'
YT_INITIAL_DATA_RE = r'(?:window\s*\[\s*["\']ytInitialData["\']\s*\]|ytInitialData)\s*=\s*({.+?})\s*;\s*(?:var\s+meta|</script|\n)'


class YouTubeComments:

    @classmethod
    def regex_search(cls, text, pattern, group=1, default=None):
        match = re.search(pattern, text)
        return match.group(group) if match else default


    @classmethod
    def ajax_request(cls, session, endpoint, ytcfg, retries=5, sleep=20):
        url = 'https://www.youtube.com' + endpoint['commandMetadata']['webCommandMetadata']['apiUrl']

        data = {'context': ytcfg['INNERTUBE_CONTEXT'], 'continuation': endpoint['continuationCommand']['token']}

        for _ in range(retries):
            response = session.post(url, params={'key': ytcfg['INNERTUBE_API_KEY']}, json=data)
            if response.status_code == 200:
                return response.json()
            if response.status_code in [403, 413]:
                return {}
            else:
                time.sleep(sleep)

    @classmethod
    def get_video_likes(cls, YOUTUBE_VIDEO_URL, sort_by=SORT_BY_RECENT, language=None, sleep=0.1):
        session = requests.Session()
        session.headers['User-Agent'] = USER_AGENT
        response = session.get(YOUTUBE_VIDEO_URL)

        if 'uxe=' in response.request.url:
            session.cookies.set('CONSENT', 'YES+cb', domain='.youtube.com')
            response = session.get(YOUTUBE_VIDEO_URL)

        html = response.text


        ytcfg = json.loads(cls.regex_search(html, YT_CFG_RE, default=''))
        if not ytcfg:
            return  # Unable to extract configuration
        if language:
            ytcfg['INNERTUBE_CONTEXT']['client']['hl'] = language

        data = json.loads(cls.regex_search(html, YT_INITIAL_DATA_RE, default=''))

    
        # Extract Video Likes from contents
        likes_contents = list(cls.search_dict(data,'defaultButtonViewModel'))
        likes = 0
        if len(likes_contents)>1:
            likes = likes_contents[1]['buttonViewModel']['title']

        return likes

    @classmethod
    def download_comments(cls, YOUTUBE_VIDEO_URL, sort_by=SORT_BY_RECENT, language=None, sleep=0.1):
        session = requests.Session()
        session.headers['User-Agent'] = USER_AGENT
        response = session.get(YOUTUBE_VIDEO_URL)

        if 'uxe=' in response.request.url:
            session.cookies.set('CONSENT', 'YES+cb', domain='.youtube.com')
            response = session.get(YOUTUBE_VIDEO_URL)

        html = response.text


        ytcfg = json.loads(cls.regex_search(html, YT_CFG_RE, default=''))
        if not ytcfg:
            return  # Unable to extract configuration
        if language:
            ytcfg['INNERTUBE_CONTEXT']['client']['hl'] = language

        data = json.loads(cls.regex_search(html, YT_INITIAL_DATA_RE, default=''))

    
        # Extract Video Likes from contents
        likes_contents = list(cls.search_dict(data,'defaultButtonViewModel'))
        likes = 0
        if len(likes_contents)>1:
            likes = likes_contents[1]['buttonViewModel']['title']

        section = next(cls.search_dict(data, 'itemSectionRenderer'), None)
        renderer = next(cls.search_dict(section, 'continuationItemRenderer'), None) if section else None
        if not renderer:
            # Comments disabled?
            return

        needs_sorting = sort_by != SORT_BY_POPULAR
        continuations = [renderer['continuationEndpoint']]
        while continuations:
            continuation = continuations.pop()
            response = cls.ajax_request(session, continuation, ytcfg)

            if not response:
                break
            if list(cls.search_dict(response, 'externalErrorMessage')):
                raise RuntimeError('Error returned from server: ' + next(cls.search_dict(response, 'externalErrorMessage')))

            if needs_sorting:
                sort_menu = next(cls.search_dict(response, 'sortFilterSubMenuRenderer'), {}).get('subMenuItems', [])
                if sort_by < len(sort_menu):
                    continuations = [sort_menu[sort_by]['serviceEndpoint']]
                    needs_sorting = False
                    continue
                raise RuntimeError('Failed to set sorting')

            actions = list(cls.search_dict(response, 'reloadContinuationItemsCommand')) + list(cls.search_dict(response, 'appendContinuationItemsAction'))
            for action in actions:
                for item in action.get('continuationItems', []):
                    if action['targetId'] == 'comments-section':
                        # Process continuations for comments and replies.
                        continuations[:0] = [ep for ep in cls.search_dict(item, 'continuationEndpoint')]
                    if action['targetId'].startswith('comment-replies-item') and 'continuationItemRenderer' in item:
                        # Process the 'Show more replies' button
                        continuations.append(next(cls.search_dict(item, 'buttonRenderer'))['command'])


            for comment in reversed(list(cls.search_dict(response, 'commentRenderer'))):
                yield {
                    'cid': comment['commentId'],
                    'text': ''.join([c['text'] for c in comment['contentText'].get('runs', [])]),
                    'time': comment['publishedTimeText']['runs'][0]['text'],
                    'author': comment.get('authorText', {}).get('simpleText', ''),
                    'channel': comment['authorEndpoint']['browseEndpoint'].get('browseId', ''),
                    'votes': comment.get('voteCount', {}).get('simpleText', '0'),
                    'photo': comment['authorThumbnail']['thumbnails'][-1]['url'],
                    'heart': next(cls.search_dict(comment, 'isHearted'), False)
                }

            time.sleep(sleep)


    @classmethod
    def search_dict(cls, partial, search_key):
        stack = [partial]
        while stack:
            current_item = stack.pop()
            if isinstance(current_item, dict):
                for key, value in current_item.items():
                    if key == search_key:
                        yield value
                    else:
                        stack.append(value)
            elif isinstance(current_item, list):
                for value in current_item:
                    stack.append(value)


    @classmethod
    def main(cls, url):
        try:
            youtube_url = url
            limit = COMMENT_LIMIT

            print('Downloading Youtube comments for video:', youtube_url)

            count = 0

            start_time = time.time()

            comments_list = []
            for comment in cls.download_comments(youtube_url):
                # comments overview
                comments_list.append(comment)
                count += 1
                if limit and count >= limit:
                    break

            print('\n[{:.2f} seconds] Done!'.format(time.time() - start_time))

            text_comments = CommentSeparator.get_comments_text(comments_list)
            likes = cls.get_video_likes(youtube_url)

            return {"likes":likes, "text_comments":list(text_comments), "comments_list":comments_list}



        except Exception as e:
            print('Error:', str(e))
            sys.exit(1)

