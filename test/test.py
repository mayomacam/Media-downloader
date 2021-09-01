import requests
import json
from pytube import YouTube
import re

headers = { 'User-Agent':  'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67' }
"""
class UIManager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.setGeometry(720, 640)
        self.setWindowTitle('Reddit-downloader')
"""
"""
# reddit single link image download
url = 'https://www.reddit.com/r/memes/comments/p1of6y/this_is_business.json'

response = requests.get(url=url, headers=headers)
#print(response.text)
print(json.loads(response.text)[0]["data"]["children"][0]["data"]["url"])
image_link = json.loads(response.text)[0]["data"]["children"][0]["data"]["url"]
d = requests.get(image_link).content
with open('download.jpg', 'wb') as file:
    file.write(d)

# reddit single video download

url = 'https://www.reddit.com/r/nextfuckinglevel/comments/p1m5jk/jesus_take_the_handlebar_and_guide_me.json'

response = requests.get(url=url, headers=headers)
#print(response.text)
print(json.loads(response.text)[0]["data"]["children"][0]["data"]["media"]["reddit_video"]["scrubber_media_url"])
video_link = json.loads(response.text)[0]["data"]["children"][0]["data"]["media"]["reddit_video"]["scrubber_media_url"]
d = requests.get(video_link).content
with open('download.mp4', 'wb') as file:
    file.write(d)


# imgur

url = 'https://www.reddit.com/r/WatchPeopleDieInside/comments/p1oq6e/this_olympic_swimmers_reaction_to_a_false_start.json'

response = requests.get(url=url, headers=headers)
#print(response.text)
print(json.loads(response.text)[0]["data"]["children"][0]["data"]["url"])
image_link = json.loads(response.text)[0]["data"]["children"][0]["data"]["url"].replace('.gifv', '.mp4')
d = requests.get(image_link).content
with open('download-imgur.mp4', 'wb') as file:
    file.write(d)
"""
"""
# gfycat

url = 'https://www.reddit.com/r/WatchPeopleDieInside/comments/ox1xyq/poor_guy.json'

response = requests.get(url=url, headers=headers)
#print(response.text)
print(json.loads(response.text)[0]["data"]["children"][0]["data"]["url"])
gfycat_url = json.loads(response.text)[0]["data"]["children"][0]["data"]["url"]
gfycat_response = requests.get(gfycat_url, headers=headers)
#print(gfycat_response.text)
data = gfycat_response.text
data = re.findall(r"[\w:\/.-]*mp4", data)[0]
print(data)
d = requests.get(data).content
with open('download-gfycat.mp4', 'wb') as file:
    file.write(d)


"""
# youtube
url = 'https://www.youtube.com/watch?v=I99BkX3sYa0&ab_channel=ShiroMaster%E2%98%86OriginalSoundtrack'

response = YouTube(url).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first().download(filename='abc.mp4')
print(response)