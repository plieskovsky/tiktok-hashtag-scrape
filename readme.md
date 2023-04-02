# tiktok hashtag scrape

Script that scrapes videos with given hashtag to a directory. It keeps track of the IDs that have been already downloaded
and doesn't download the same videos again.

## Pre-Requisites
1. Python3
2. pip must be installed
3. `cookies.json` file that will be used for scraping the videos

### cookies.json
To get this file you can use CookieManager browser extension. Just log into your tiktok account and
export all the cookies into a json file.

### After Installing these run following commands in terminal:

`1. pip install TikTokApi`
`2. pyppeteer-install`
`3. pip install PyDrive`


## How to Run Script?

You have to provide:
1. directory to which the videos will be downloaded
2. hashtags from which we want to download the videos
3. `cookies.json` has to be located in the directory that we pass as argument

The directory doesn't have to exist. So for example if we want to use
`/Users/youruser/videos` only `/Users/youruser/tkyt` has to exist.
The script will configure all the needed directories and files automatically, except for `cookies.json`.
That file has to be copied into the directory manually after the first script run initializes it.

```
python3 tiktok-hashtag-scrape.py /Users/youruser/videos funny,kids
```

## Limitations
1. It currently downloads videos to fulfill 6 minutes of video. The sum of downloaded video durations is saved to a
`<path-arg>videos/current_duration.txt` file. In order to download again after hitting the 10 minutes
the content of this file has to be overwritten to `0`.
2. In case the download return `403` HTTP code the info is logged and file download skipped. TikTok uses 403 to prevent
private video downloads. 
3. Tiktok has rate limitting in place, if you encounter responses saying that you need to log into your account you most probably hit the rate limiting. To me scraping the videos twice a day seems to work ok without being rate limited.
