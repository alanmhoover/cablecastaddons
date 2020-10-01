import configparser
import sys
import http.client
import json
import base64

API = '/cablecastapi/v1/'
config = configparser.ConfigParser()
config.read('./cablecastconfig.ini')
config_user = config['cablecast']['userid']
config_pass = config['cablecast']['passwd']
config_ip = config['cablecast']['server_ip']

VIDEO_SERVER = config['formats']['video_server']
NETWORK_STREAM = config['formats']['network_stream']

# arg = '68813'   ## Randi Rhodes
# arg = '70023'   ## Laura Flanders
# arg = '70027'   ## Rick Smith
arg = sys.argv[1]

def make_authorization(userid=None, password=None):
    if userid is None:
        userid = config_user
    if password is None:
        password = config_pass
    auth = f'{userid}:{password}'.encode()
    tok = base64.b64encode(auth).decode()
    return 'Basic  ' + tok

def make_headers(userid=None, password=None):
    return {'Authorization' : make_authorization(userid, password),
            'Content-Type' : 'application/json'}

def get_url(connection, gppd, url, body= None, headers=None):
    if headers and body:
        connection.request(gppd, url, body=body, headers=headers)
    else:
        connection.request(gppd, url)
    r1 = connection.getresponse()
#     print(r1.status)
    return json.loads((r1.read()))

conn = http.client.HTTPConnection(config_ip)

res = get_url(conn, 'GET',f'{API}shows/search/advanced/{arg}')
showid = res['savedShowSearch']['results'][0]
print(f'Show : {showid}')
res = get_url(conn,'GET',f'/cablecastapi/v1/shows/{showid}')
reel = res['show']['reels'][0]
res = get_url(conn, 'GET', f'{API}reels/{reel}')
length1 = res['reel']['length']
digitalfile = res['reel']['digitalFiles'][0]
media = res['reel']['media']
res = get_url(conn, 'GET',f'{API}media/{media}')
# print(res)
# print(digitalfile)
format = res['media']['format']
if int(format) == int(NETWORK_STREAM):
    res['media']['format'] = VIDEO_SERVER
    res = get_url(conn, 'PUT',f'{API}media/{media}', body=json.JSONEncoder().encode(res), headers=make_headers())
    res = get_url(conn, 'GET',f'{API}digitalfiles/{digitalfile}')
#     print(res)
    length2 = res['digitalFile']['mediaInfo']['media']['track'][0]['Duration']

    res = get_url(conn, 'GET',f'{API}reels/{reel}')
    length1 = int(res['reel']['length'])
    length2 = int(float(length2))
#     print(res)
    print(length1, length2)
    if length1 != length2:
        print('Updating show length')
        res['reel']['length'] = length2
        res = get_url(conn, 'PUT',f'{API}reels/{reel}', body=json.JSONEncoder().encode(res), headers=make_headers())
