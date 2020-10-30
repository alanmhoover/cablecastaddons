import configparser
import json
import base64
import http.client

API = '/cablecastapi/v1/'
config = configparser.ConfigParser()
config.read('./cablecastconfig.ini')
config_user = config['cablecast']['userid']
config_pass = config['cablecast']['passwd']
config_ip = config['cablecast']['server_ip']

VIDEO_SERVER = config['formats']['video_server']
NETWORK_STREAM = config['formats']['network_stream']

OUTPUT_DIRECTORY = config['downloader']['destination_folder']
FORMAT = config['downloader']['format']
DL_SEARCH = config['downloader']['search_number']

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
    return json.loads(r1.read())
