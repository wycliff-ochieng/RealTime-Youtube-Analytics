import  requests
import yaml
import json
from pprint import pprint
from kafka import KafkaProducer
import logging

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

logging.basicConfig(level=logging.INFO)

def fetch_page(url,parameters,page_token='None'):
    params = {
        **parameters,'key':api_key,'page_token':page_token
    }
    videos = requests.get(url,params)
    payload = json.loads(videos.text)
    logging.info("response=>%s", payload)
    return payload

def fetch_page_list(url,parameters,page_token=None):
    while True:
        payload = fetch_page(url,parameters,page_token)
        yield from payload['items']

        page_token = payload.get('nextPageToken')
        if page_token is None:
            break

def format_response(vids):
    vids_res = {
            'title':vids['snippet']['title'],
            'timePublished':vids['snippet']['publishedAt'],
            'likes':vids['statistics'].get('likeCount',0),
            'comments':vids['statistics'].get('commentCount',0),
            'views':vids['statistics'].get('viewCount',0),
            'tags':vids['snippet'].get('tags[0:2]')
            }
    return vids_res

if __name__=="__main__":

    """producer = KafkaProducer(bootstrap_servers =['localhost:9092'])
    
    api_key = config['youtube']['api_key']
    videos = requests.get('https://www.googleapis.com/youtube/v3/videos',
                      {
                          'key':api_key,
                          'id':'r39z7CX1tZo',
                          'part':'snippet,statistics,status'
                      })
    #print(videos.text)
    response = json.loads(videos.text)['items']
    for vids in response:
        vids_res = {
            'title':vids['snippet']['title'],
            'timePublished':vids['snippet']['publishedAt'],
            'likes':vids['statistics'].get('likeCount',0),
            'comments':vids['statistics'].get('commentCount',0),
            'views':vids['statistics'].get('viewCount',0),
            'tags':vids['snippet']['tags'][0:2]
            }
        
    print(pprint(vids_res))
    producer.send('youtube_videos',json.dumps(vids_res).encode('utf-8'))
    producer.flush()"""

    api_key = config['youtube']['api_key']
    playlist_id = config['youtube']['playlist_id']
    """videos = requests.get('https://www.googleapis.com/youtube/v3/playlistItems',
                      {
                          'key':api_key,
                          'playlistId':playlist_id,
                          'part':'snippet,contentDetails,status',
                          'page_token':'EAAaHlBUOkNBVWlFREV5UlVaQ00wSXhRelUzUkVVMFJURQ'
                      })
    print(videos.text)"""

    for video_items in fetch_page_list(
        "https://www.googleapis.com/youtube/v3/playlistItems",
        {'playlist_id':playlist_id,'part':'snippet,contentDetails,status'},None
    ):
        video_id = video_items['contentDetails']['videoId']
        for video in fetch_page_list(
            "https://www.googleapis.com/youtube/v3/videos",{
            'id':video_id,'part':'snippet,statistics'
        },None):
            logging.info("video here =>%s",pprint(format_response(video)))


