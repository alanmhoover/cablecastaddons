import http.client
import datetime
import configparser

import json
# import urllib.request
FORMAT = '480'
OUTPUT_DIRECTORY = 'E:'

config = configparser.ConfigParser()
config.read('./cablecastconfig.ini')
config_ip = config['cablecast']['server_ip']

today = datetime.date.today()
filename = f'dn{today.year}-{today.month:02}{today.day:02}'
#  get info from cablecast
conn = http.client.HTTPConnection(config_ip)
conn.request('GET','/cablecastapi/v1/shows/search/advanced/35298')
r1 = conn.getresponse()
print(r1.status, r1.reason)
res = json.loads((r1.read()))
# print(res)
showid = res['savedShowSearch']['results'][-1]
showid = str(showid) + '-1 '

print(showid)
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

# statconn = http.client.HTTPSConnection("www.democracynow.org")
# statconn.request("GET",'/static')
# r1 = statconn.getresponse()
# print(r1.status, r1.reason)

conn = http.client.HTTPSConnection("www.democracynow.org")
conn.request("GET",caption_file_location)

r1 = conn.getresponse()
print(r1.status, r1.reason)
if r1.status == 200:
    with open(f"{OUTPUT_DIRECTORY}{showid}{filename}.scc",mode="wb") as outfile:
        outfile.write(r1.read())
# with urllib.re(f"https://www.democracynow.org{caption_file_location}") as response:
#     with open(f"{filename}.scc",mode="wb") as outfile:
#         outfile.write(response.read())

if FORMAT == '360':
    conn = http.client.HTTPSConnection("publish.dvlabs.com")
    conn.request("GET",mpeg_file_location)
elif FORMAT == '480':
    conn = http.client.HTTPConnection("mpeg.democracynow.org")
    conn.request("GET",mpeg_file_location)

r1 = conn.getresponse()
print(r1.status, r1.reason)
if r1.status == 200:
    with open(f"{OUTPUT_DIRECTORY}{showid}{filename}.{extension}",mode="wb") as outfile:
        outfile.write(r1.read())
