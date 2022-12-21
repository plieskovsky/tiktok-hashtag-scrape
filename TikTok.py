import os
import sys
import time
import zipfile
import requests
import json

from TikTokApi import *


# not working ATM!!! https://github.com/davidteather/TikTok-Api/issues/948

# def zipdir(path, ziph):
#     # Fucntion to Zip the folder
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             ziph.write(os.path.join(root, file))

# api = TikTokApi()

# has also offset so will use that later :)
# videos = api.hashtag(name='gym').videos(1)
#
# for tiktok in videos:
#     print("sleeping 3 sec before next download")
#     time.sleep(3)
#
#     print("video info:" + tiktok.info())
#     bytess = api.video.bytes()
#     with open('saved_video.mp4', 'wb') as output:
#         output.write(bytess)

# zipf = zipfile.ZipFile(hashtag + '.zip', 'w', zipfile.ZIP_DEFLATED)
# zipdir(hashtag+"/", zipf)
# zipf.close()

