# Json Response https://m.tiktok.com/share/item/list?id=&type=5&count=48&minCursor=0&maxCursor=0&_signature=z9nIxxAWkszGlbLSXGTDqM.ZyN
# obj -> body -> itemListData -> itemListData[i] -> itemInfos -> video -> urls[0] gives downloadable url
import requests
import random
import string
import urllib.request
import glob
import os
import mimetypes
from TikTokApi import TikTokapi


def clearTMP(delpath):
    r = glob.glob(delpath)
    for i in r:
        os.remove(i)


clearTMP('output/output.mp4')

# Vars
count = 30
api = TikTokapi("browsermob-proxy/bin/browsermob-proxy")

results = api.trending(count=count)
prevloops = 0
for res in results:
    r = requests.get(res["itemInfos"]["video"]["urls"][0], allow_redirects=False)
    content_type = r.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    open('downloaded/' + str(prevloops) +
            extension, "wb").write(r.content)
    open("downloaded/concat.txt", 'a').write("file " +
                                                str(prevloops) + ".mkv" + "\n")
    os.system("ffmpeg -loglevel panic -i downloaded/" + str(prevloops) +
                extension + " -c copy -map 0 downloaded/" + str(prevloops) + ".mkv")
    prevloops += 1

api.quit_browser()

# concat errors
# ffmpeg -f concat -i downloaded/concat.txt -safe 1 -r 30 -fflags +genpts -c:a copy output.mp4
os.system("ffmpeg -f concat -i downloaded/concat.txt -safe 1 -r 30 -fflags +genpts -c:a copy downloaded/output.mp4")
os.system('''ffmpeg -loglevel error -r 30 -i resources/bkg.png -i downloaded/output.mp4 -b:v 1M -filter_complex ''' +
          '''"[1:v]scale=''' + "750" +
          ''':''' + "1080" + ''' [ovrl], [0:v][ovrl]overlay=(main_w-overlay_w)/2:((main_h-overlay_h)/2)"''' +
          ''' output/output.mp4''')


clearTMP('downloaded/*')
