import sys
import http.client
import json
import base64
import ccapi

# arg = '68813'   ## Randi Rhodes
# arg = '70023'   ## Laura Flanders
# arg = '70027'   ## Rick Smith
arg = sys.argv[1]

conn = http.client.HTTPConnection(ccapi.config_ip)

res = ccapi.get_url(conn, 'GET',f'{ccapi.API}shows/search/advanced/{arg}')
showid = res['savedShowSearch']['results'][0]
print(f'Show : {showid}')
res = ccapi.get_url(conn,'GET',f'{ccapi.API}shows/{showid}')
reel = res['show']['reels'][0]
res = ccapi.get_url(conn, 'GET', f'{ccapi.API}reels/{reel}')
length1 = res['reel']['length']
digitalfile = res['reel']['digitalFiles'][0]
media = res['reel']['media']
res = ccapi.get_url(conn, 'GET',f'{ccapi.API}media/{media}')
# print(res)
# print(digitalfile)
format = res['media']['format']
if int(format) == int(ccapi.NETWORK_STREAM):
    res['media']['format'] = ccapi.VIDEO_SERVER
    res = ccapi.get_url(conn, 'PUT',f'{ccapi.API}media/{media}', 
        body=json.JSONEncoder().encode(res), headers=ccapi.make_headers())
    res = ccapi.get_url(conn, 'GET',f'{ccapi.API}digitalfiles/{digitalfile}')
#     print(res)
    length2 = res['digitalFile']['mediaInfo']['media']['track'][0]['Duration']

    res = ccapi.get_url(conn, 'GET',f'{ccapi.API}reels/{reel}')
    length1 = int(res['reel']['length'])
    length2 = int(float(length2))
#     print(res)
    print(length1, length2)
    if length1 != length2:
        print('Updating show length')
        res['reel']['length'] = length2
        res = ccapi.get_url(conn, 'PUT',f'{ccapi.API}reels/{reel}', 
            body=json.JSONEncoder().encode(res), headers=ccapi.make_headers())
