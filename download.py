#!/usr/local/bin/python3
import http.client
import datetime
import configparser

FORMAT = '480'

config = configparser.ConfigParser()
config.read('./cablecastconfig.ini')
config_ip = config['cablecast']['server_ip']

today = datetime.date.today()
filename = f'dn{today.year}-{today.month:02}{today.day:02}'

print(filename)
caption_file_location = f"/scc/{filename}.scc"
# print(caption_file_location)
if FORMAT == '360':
    mpeg_file_location = f"/democracynow/360/{filename}.mp4"
    extension = 'mp4'
elif FORMAT == '480':
    mpeg_file_location = f"/{filename}.mp4"
    extension = 'mp4'
print(mpeg_file_location)

conn = http.client.HTTPSConnection("www.democracynow.org")
conn.request("GET",caption_file_location)

r1 = conn.getresponse()
print(r1.status, r1.reason)
if r1.status == 200:
    with open(f"{filename}.scc",mode="wb") as outfile:
        outfile.write(r1.read())

if FORMAT == '360':
    conn = http.client.HTTPSConnection("publish.dvlabs.com")
    conn.request("GET",mpeg_file_location)
elif FORMAT == '480':
    conn = http.client.HTTPConnection("mpeg.democracynow.org")
    conn.request("GET",mpeg_file_location)

r1 = conn.getresponse()
print(r1.status, r1.reason)
if r1.status == 200:
    with open(f"{filename}.{extension}",mode="wb") as outfile:
        outfile.write(r1.read())
