import json
import os
import traceback

import requests
import urllib.request
import time
from pathlib import Path

# TODO PROJECT LEVEL:
# caller func should be able to reset the duration counter to zero & also remove all vids once the video is done and uploaded
# after that we can start scraping vids again


def get_cookies_from_file():
    with open('cookies.json') as f:
        cookies = json.load(f)

    cookies_kv = {}
    # Just use the name and the value properties
    for cookie in cookies:
        cookies_kv[cookie['name']] = cookie['value']
    return cookies_kv


def fetch_vids_info(keyword, offset=0):
    params = {
        'keyword': keyword,
        'offset': offset,
        #     maybe they do have also some param for size? so we could load like 30 at once :)
    }
    response = requests.get("http://us.tiktok.com/api/search/item/full/", params=params,
                            cookies=get_cookies_from_file())
    return response.json()


def prepare_files(hashtag):
    my_file = Path(hashtag)
    if not my_file.exists():
        os.mkdir(hashtag)
        os.mkdir(hashtag + "/videos")
        open(hashtag + "/videos/current_duration.txt", 'a').close()
        open(hashtag + "/ids.txt", 'a').close()


def parse_duration(hashtag):
    with open(hashtag + "/videos/current_duration.txt") as f:
        lines = f.readlines()
        if len(lines) == 0:
            return 0

        return int(lines[0])


def parse_ids(hashtag):
    idsSet = set()
    with open(hashtag + "/ids.txt") as f:
        for line in f.readlines():
            idsSet.add(line.replace("\n", ""))

    return idsSet


# hashtag should be configurable :)
try:
    hashtag = "gym"
    prepare_files(hashtag)
    seconds = parse_duration(hashtag)
    ids = parse_ids(hashtag)

    offset = 0
    # download until we have 10 min of videos
    while seconds < 10 * 60:
        response = fetch_vids_info("#" + hashtag, offset)
        for vid in response['item_list']:
            if seconds < 10 * 60:
                break

            id = vid["id"]
            vidDetails = vid['video']
            downAddr = vidDetails['downloadAddr']

            # ignore videos that have been already used
            if id in ids:
                continue

            # use only mp4 files
            if vidDetails['format'] != 'mp4':
                continue

            # use only short clips
            duration = vidDetails['duration']
            if duration > 25:
                continue

            print("downloading " + vid['desc'])
            # name = 'video' + id + '.mp4'
            # urllib.request.urlretrieve(downAddr, name)

            seconds += duration
            # persist new id and duration
            with open(hashtag + "/videos/current_duration.txt", "w") as f:
                f.write(str(seconds))
            with open(hashtag + "/ids.txt", "a") as f:
                f.write(id + "\n")

        # finish up when there are no more records available
        hasMore = response['has_more']
        if not hasMore == 1:
            break

        offset = response['cursor']
        print("has more: ", hasMore, ",new offset:", offset)
        time.sleep(5)

except BaseException as e:
    print('An exception occurred: {}'.format(e))
    traceback.print_exc(e)
    exit(555)
