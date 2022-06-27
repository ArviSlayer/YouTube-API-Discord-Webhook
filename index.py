import os
import json
import googleapiclient.discovery
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime, time
from time import sleep

previousVideo = False


with open('keys.json') as json_file:
    key = json.load(json_file)

startTime = key["startTime"]
endTime = key["endTime"]


api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = key["APIKey"]
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey= DEVELOPER_KEY)


vidRequest = youtube.search().list(
    part="snippet",
    channelId=key["channelID"],
    maxResults=2,
    order="date",
    type="video"
)


webhook = DiscordWebhook(url=key["webhook"])


def discordPing(title, description, url):
    webhook.content = "@everyone **Yeni Video Yayında** \n" + title + "\n" + description + "\n" + url
    webhook.execute()
    print("Sunucuya Bildirim Gönderildi")


def intialize():
    data = vidRequest.execute()
    print(data)
    global previousVideo
    previousVideo = data["items"][0]["id"]["videoId"]
    print(data["items"][0]["snippet"]["title"])
    print(previousVideo)


def checkVideo():
    global previousVideo
    data = vidRequest.execute()
    workingVideo = data["items"][0]["id"]["videoId"]
    print("Video Kontrol Ediliyor")

  
    if workingVideo != previousVideo:
        print("Yeni Video Bulundu")
        
        title = data["items"][0]["snippet"]["title"].replace("&#39;", "'")
        
        description = data["items"][0]["snippet"]["description"].split("-")[0]
        url = "https://youtu.be/" + workingVideo
       
        discordPing(title, description, url)
        print(previousVideo)
        
        previousVideo = workingVideo
        return

def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else:
        return start <= now or now < end


def checkTime():

    if in_between(datetime.now().time(), time(int(startTime.split(":")[0]), int(startTime.split(":")[1])), time(int(endTime.split(":")[0]), int(endTime.split(":")[1]))):
        print("Çok Fazla Zaman Kaybettin, İşlem Zaman Aşımına Uğradı")
        return True

    else:
        print("Videoyu Kontrol Etmek İçin İstenilen Zaman Yanlış")
        print("Doğru Zaman: " + startTime)
        return False

intialize()

while True:
   
    if checkTime():
        print(previousVideo)
        checkVideo()
        print(previousVideo)
    sleep(int(key["delay"]))
