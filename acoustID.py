import os
import subprocess
import requests
import sys
import time
import itertools
import threading

done = False
animation = ['∙ ∙ ∙ ∙ ∙ ∙ ∙', ' ∙∙ ∙ ∙ ∙ ∙ ∙', '∙  ∙∙ ∙ ∙ ∙ ∙', '∙ ∙  ∙∙ ∙ ∙ ∙',
             '∙ ∙ ∙  ∙∙ ∙ ∙', '∙ ∙ ∙ ∙  ∙∙ ∙', '∙ ∙ ∙ ∙ ∙  ∙∙', '∙ ∙ ∙ ∙ ∙ ∙ ∙',
             '∙ ∙ ∙ ∙ ∙ ∙∙ ', '∙ ∙ ∙ ∙ ∙∙  ∙', '∙ ∙ ∙ ∙∙  ∙ ∙', '∙ ∙ ∙∙  ∙ ∙ ∙',
             '∙ ∙∙  ∙ ∙ ∙ ∙', '∙∙  ∙ ∙ ∙ ∙ ∙']


def animate():
    for an in itertools.cycle(animation):
        if done:
            break
        sys.stdout.write('\r'+an)
        sys.stdout.flush()
        time.sleep(0.2)


base = "https://api.acoustid.org/v2/lookup"
client = 'AcoustID API Key'


def Exit(reason):
    print(reason)
    exit(420)


def getprint(media):
    finger = subprocess.run(['fpcalc', media], stdout=subprocess.PIPE)
    out = finger.stdout.decode('utf-8').split('\r\n')
    if out[0:5] == 'ERROR':
        Exit(str('fpcalc error: '+out.split(': ')[1]))
    duration = out[0].split('=')[1]
    fprint = out[1].split('=')[1]
    return [duration, fprint]


def lookup(file):
    # check for an internet connection
    while True:
        try:
            requests.get('https://acoustid.org/webservice')
            break
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            Exit("Can't reach AcoustID.")
    fingerprint = getprint(file)
    lookup_id = base + "?client=" + client + '&duration=' + fingerprint[0] + '&fingerprint=' + fingerprint[1]
    raw_id = requests.get(lookup_id)
    if not raw_id.json()["status"] == 'ok':
        Exit(str("Acoust ID Error: status " + raw_id.json()["status"]))
    if len(raw_id.json()['results']) == 0:
        Exit("No matches found.")
    acoust_id = raw_id.json()["results"][0]["id"]
    score = float(raw_id.json()["results"][0]["score"]) * 100
    lookup_song = base + "?client=" + client + '&meta=recordings&trackid=' + acoust_id
    raw_song = requests.get(lookup_song)
    title = raw_song.json()['results'][0]['recordings'][0]['title']
    mbz = raw_song.json()['results'][0]['recordings'][0]['id']
    artist = raw_song.json()['results'][0]['recordings'][0]['artists'][0]['name']
    return [artist, title, mbz, score]


if not len(sys.argv) == 1:
    if str(sys.argv[1]) == '-h' or str(sys.argv[1]) == '--help':
        print("AcoustID Wrapper\nusage: acoustID.py file\n\nIdentifies the Title and Artist of <file> using AcoustID")
        Exit("")
    if os.path.isfile(str(sys.argv[1])):
        t = threading.Thread(target=animate)
        t.start()
        details = lookup(sys.argv[1])
        done = True
        sys.stdout.write('\r' + ' ' * 15 + '\r')
        print("'"+details[1] + "' by " + details[0])
        print("https://www.musicbrainz.org/recording/"+details[2]+"\nPowered by AcoustID - https://acoustid.org/")
    else:
        print('File not found: '+sys.argv[1])
