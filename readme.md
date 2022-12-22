# tiktok hashtag scrape

Script that scrapes videos with given hashtag to a directory. It keeps track of the IDs that have been already downloaded
and doesn't download the same videos again.
Downloads only videos to fulfill 10 minutes of video.

## Pre-Requisites
1. Python3
2. pip must be installed

### After Installing these run following commands in terminal:

`1. pip install TikTokApi`
`2. pyppeteer-install`
`3. pip install PyDrive`


### How to Run Script?

U have to provide:
- directory to which the videos will be downloaded
- hashtags from which we want to download the videos

The directory doesn't have to exist. So for example if we want to use
`/Users/plieskovsky/tkyt/gym` only `/Users/plieskovsky/tkyt` has to exist.
The script will configure all the needed directories and files automatically.

```
python3 test.py /Users/plieskovsky/tkyt/gym gym,muscle
```
