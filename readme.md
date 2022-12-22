
# TikTok API in Python

This is an unofficial api wrapper for TikTok.com in python. With this api you are able to call most trending and fetch specific user information. The user videos will be stored as .zip file and will be automatically uploaded to Google Drive.

## Pre-Requits
1. Python3
2. pip must be installed
3. Google Drive Api must be configured and download json package and name it client_secrets.json

### After Installing these run following commands in terminal:

`1. pip install TikTokApi`
`2. pyppeteer-install`
`3. pip install PyDrive`


### How to Run Script?

U have to provide:
- directory to which the videos will be downloaded
- hashtags from which we want to download the videos

```
python3 test.py /Users/plieskovsky/tkyt/gym gym,muscle
```
