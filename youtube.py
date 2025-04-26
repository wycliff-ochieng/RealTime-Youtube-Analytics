import  requests
import yaml
import json
from pprint import pprint

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

if __name__=="__main__":
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

