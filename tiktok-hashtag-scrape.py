import json
import os
import random
import shutil
import sys
import logging
from requests import ReadTimeout, ConnectTimeout, Timeout


import requests
import urllib.request
import time
from pathlib import Path


def prepare_files(dirPath):
    my_file = Path(dirPath)
    if not my_file.exists():
        os.mkdir(dirPath)
        os.mkdir(dirPath + "/videos")
        open(dirPath + "/videos/current_duration.txt", 'a').close()
        open(dirPath + "/ids.txt", 'a').close()


def contains_hashtag(hashtags, description):
    for hashtag in hashtags:
        if hashtag in description:
            return True
    return False


def parse_duration(dirPath):
    with open(dirPath + "/videos/current_duration.txt") as f:
        lines = f.readlines()
        if len(lines) == 0:
            return 0

        return int(lines[0])


def parse_ids(dirPath):
    idsSet = set()
    with open(dirPath + "/ids.txt") as f:
        for line in f.readlines():
            idsSet.add(line.replace("\n", ""))

    return idsSet


def parse_hashtags(hashtags):
    return str(hashtags).split(",")


def get_cookies_from_file(path):
    with open(path + '/cookies.json') as f:
        cookies = json.load(f)

    cookies_kv = {}
    # Just use the name and the value properties
    for cookie in cookies:
        cookies_kv[cookie['name']] = cookie['value']
    return cookies_kv


def fetch_vids_info(path, keyword, cookies, offset=0, tries=1):
    params = {
        'keyword': keyword,
        'offset': offset,
    }

    for i in range(tries):
        try:
            resp = requests.get("http://us.tiktok.com/api/search/item/full/", params=params,
                                cookies=cookies, timeout=3)
            return resp.json()
        except (ConnectTimeout, ReadTimeout, Timeout):
            if i < tries - 1:
                logging.warning("Retrying to fetch videos due to error, try: '%d'", i)
                continue
            else:
                raise
        except ConnectionResetError:
            if i < tries - 1:
                logging.warning("Retrying to fetch videos due to connection reset error, try: '%d'", i)
                continue
            else:
                raise


def download_vid(ulr, path, cookies, tries=1):
    for i in range(tries):
        try:
            headers = {'referer': 'https://www.tiktok.com/'}
            req = requests.get(ulr, headers=headers, cookies=cookies, timeout=3, stream=True)
            # non 200 status code
            if req.status_code >= 300:
                logging.error("HTTP error '%d' response, removing file if present", req.status_code)
                if os.path.exists(filePath):
                    os.remove(filePath)
                if req.status_code == 403:
                    logging.error("403 error code - ignoring and continuing download")
                    return False
                else:
                    # non 403 HTTP responses
                    if i < tries - 1:
                        logging.warning("Retrying to download videos due to response '%d', try: '%d'", req.status_code, i)
                        time.sleep(5)
                        continue
                    else:
                        raise Exception("Unexpected video download response code: "+req.status_code)

            # Open the output file and make sure we write in binary mode
            with open(path, 'wb') as fh:
                for chunk in req.iter_content(1024 * 1024):
                    fh.write(chunk)
            return True

        except (ConnectTimeout, ReadTimeout, Timeout):
            if i < tries - 1:
                logging.warning("Retrying to download videos due to timeout, try: '%d'", i)
                continue
            else:
                raise
        except ConnectionResetError:
            if i < tries - 1:
                logging.warning("Retrying to fetch videos due to connection reset error, try: '%d'", i)
                continue
            else:
                raise


try:
    video_seconds = 6*60
    directory = sys.argv[1]
    hashtags = parse_hashtags(sys.argv[2])

    random.shuffle(hashtags)
    prepare_files(directory)
    seconds = parse_duration(directory)
    ids = parse_ids(directory)
    cookies = get_cookies_from_file(directory)

    logging.basicConfig(format='%(asctime)s %(process)d - %(levelname)s - %(message)s',
                        stream=sys.stdout,
                        level=logging.INFO)

    # iterate over all the hashtags if needed
    for hashtag in hashtags:
        offset = 0

        # download until we have desired video lenght
        while seconds < video_seconds:
            logging.info("fetching videos for hashtag '%s' and offset '%d'", hashtag, offset)
            response = fetch_vids_info(directory, "#" + hashtag, cookies, offset, tries=10)

            if response["status_code"] == 2483:
                logging.error("Fetch videos returned not logged code: 2483 - stopping execution")
                logging.error(response)
                sys.exit(3)

            # if response doesn't contain item_list log and continue with another hashtag
            if "item_list" not in response:
                logging.warning("item_list not found in response for hashtag '%s'", hashtag)
                break

            for vid in response['item_list']:
                if seconds > video_seconds:
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

                # use only videos that contain one of the hashtags in the description
                if not contains_hashtag(hashtags, vid['desc']):
                    continue

                # use only proper width and height videos
                width = vidDetails["width"]
                height = vidDetails["height"]
                if height < 1000 or height > 1100 or width < 530 or width > 630:
                    continue

                filePath = directory + "/videos/" + id + '-raw.mp4'
                try:
                    logging.info("downloading " + vid['desc'])
                    success = download_vid(downAddr, filePath, cookies, tries=10)
                    # if video response was 403 add to ids list and continue
                    if not success:
                        # add to the ids list and continue
                        with open(directory + "/ids.txt", "a") as f:
                            f.write(id + "\n")
                        continue

                except BaseException as e:
                    logging.error("Exception occurred when downloading - removing file if present", exc_info=True)
                    if os.path.exists(filePath):
                        os.remove(filePath)
                    sys.exit(4)

                seconds += duration
                # persist new id and duration
                with open(directory + "/videos/current_duration.txt", "w") as f:
                    f.write(str(seconds))
                with open(directory + "/ids.txt", "a") as f:
                    f.write(id + "\n")

            offset = response['cursor']
            logging.info("moving request offset for hashtag '%s' to '%d'", hashtag, offset)
            time.sleep(5)

    if seconds < video_seconds:
        logging.warning("could not find enough videos to make '%d' seconds compilation", video_seconds)
        sys.exit(2)

except BaseException as e:
    logging.error("Exception occurred", exc_info=True)
    sys.exit(1)
