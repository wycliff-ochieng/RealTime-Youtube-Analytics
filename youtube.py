import  requests
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

if __name__=="__main__":
    api_key = config['youtube']['api_key']
    videos = requests.get('https://www.googleapis.com/youtube/v3/videos',
                      {
                          'key':api_key,
                          'id':'-368VzqcjSo&list=PL0xRBLFXXsP5PwGwZkSOhPFbvoUUKQJat',
                          'part':'snippet,statistics,status'
                      })
    print(videos.text)

