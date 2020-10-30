import http.client
import json
import sys
import base64
from tkinter import filedialog
import ccapi

# a) get chapters input file
# 1) get v1/shows/{showid}
# 2) vod <- res['shows']['vods'][0]
# b) parse line of file to get time; title/body
# c) build dict for new chapter
# 3) post v1/chapters
# 4) put v1/vods{vod}  to publish chapters

def get_showid(input_line):
    first_line = input_line.split()
    try:
        showid = int(first_line[0].strip())
    except ValueError:
        return 0
    # print(showid)
    return showid

def calc_time(in_time):
    times = in_time.split(':')
    hrs, mins = 0, 0
    if len(times) == 1:
        secs = int(times[0])
    elif len(times) == 2:
        secs = int(times[1]) 
        if len(times[0]) > 0:
            mins = int(times[0])
    else : #len(times) == 3
        secs = int(times[2])
        mins = int(times[1])
        if len(times[0]) > 0:
            hrs = int(times[0])
    return (hrs * 3600) + (mins * 60) + secs

def make_empty_chapter():
    return {'vod' : 0,
            'title' : '',
            'body' : '',
            'operatorNote' : '',
            'offset' : 0,
            'quickAdded' : False,
            'order' : None,
            "deleted" : False
            }

def get_file_name():
    return filedialog.askopenfilename(#initial_dir='/',
        title='Select File to Import', 
        filetypes=(('Chapters files','*.chp'), ('txt files','*.txt'),  
            ('all files','*.*')))

conn = http.client.HTTPConnection(ccapi.config_ip)

file_name = get_file_name()
# print(file_name)
if not file_name: sys.exit()
with open(file_name,'r') as input_data:
    showid = get_showid(input_data.readline())
    res = ccapi.get_url(conn,'GET',f'{ccapi.API}shows/{showid}')
    chap = make_empty_chapter()
    vod = res['show']['vods'][0]
    chap['vod'] = vod
    payload = {'chapter': chap}
    for row in input_data:
        items = row.split()
        chap['offset'] = calc_time(items[0])
        desc = ' '.join(items[1:]) 
        chap['body'] = desc
        chap['title'] = desc[:50]
        print(desc)
        print(payload)
        #  write chapter to database
        res = ccapi.get_url(conn, 'POST',f'{ccapi.API}chapters', 
            body=json.JSONEncoder().encode(payload), 
            headers=ccapi.make_headers())
        print(res)

    # Publish the chapters
    res = ccapi.get_url(conn, 'GET', f'{ccapi.API}vods/{vod}')
    # print(res)
    res['vod']['chaptersPublished'] = True
    res = ccapi.get_url(conn, 'PUT' , f'{ccapi.API}vods/{vod}', 
                body=json.JSONEncoder().encode(res), 
                headers=ccapi.make_headers())
    # print(res)