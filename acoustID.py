import os
import subprocess
import requests
import sys
import time
import itertools
import threading

done = False
cmd = False

animation = ['.   ', '..  ', '... ', ' .. ', '  . ']


def animate():
    for an in itertools.cycle(animation):
        if done:
            break
        sys.stdout.write('\r'+an)
        sys.stdout.flush()
        time.sleep(0.1)


base = "https://api.acoustid.org/v2/lookup"
client = 'bZoX2TyccH'  # AcoustID API Key


def Exit(reason):
    print(reason)
    exit(420)


def getprint(media):
    global cmd
    try:
        finger = subprocess.run(['fpcalc', media], stdout=subprocess.PIPE)
        out = finger.stdout.decode('utf-8').split('\r\n')
    except FileNotFoundError:
        return None
    if out[0:5] == 'ERROR':
        if cmd:
            Exit(str('fpcalc error: '+out.split(': ')[1]))
        else:
            return None
    duration = out[0].split('=')[1]
    fprint = out[1].split('=')[1]
    return [duration, fprint]


def lookup(file):
    global cmd
    while True:
        try:
            requests.get('https://acoustid.org/webservice')
            break
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if cmd:
                Exit("Can't reach AcoustID.")
            else:
                return 'ERROR: NO INTERNET ACCESS'
    fingerprint = getprint(file)
    if fingerprint is None:
        return 'ERROR: FPCALC ERROR'
    lookup_id = base + "?client=" + client + '&duration=' + fingerprint[0] + '&fingerprint=' + fingerprint[1]
    raw_id = requests.get(lookup_id)
    if not raw_id.json()["status"] == 'ok':
        if cmd:
            Exit(str("Acoust ID Error\n" + raw_id.json()["status"]))
        else:
            return 'ERROR: ACOUSTID ERROR'
    if len(raw_id.json()['results']) == 0:
        if cmd:
            Exit("No matches found.")
        else:
            return 'ERROR: NO MATCHES FOUND'
    acoust_id = raw_id.json()["results"][0]["id"]
    score = float(raw_id.json()["results"][0]["score"]) * 100
    lookup_song = base + "?client=" + client + '&meta=recordings&trackid=' + acoust_id
    raw_song = requests.get(lookup_song)
    title = raw_song.json()['results'][0]['recordings'][0]['title']
    mbiz = raw_song.json()['results'][0]['recordings'][0]['id']
    artist = raw_song.json()['results'][0]['recordings'][0]['artists'][0]['name']
    return [artist, title, mbiz, score]


if __name__ == '__main__':
    if not len(sys.argv) == 1:
        if str(sys.argv[1]) == '-h' or str(sys.argv[1]) == '--help':
            print(
                "AcoustID Wrapper\nusage: acoustID.py file\n\nIdentifies the Title and Artist of <file> using AcoustID")
            Exit("")
        if os.path.isfile(str(sys.argv[1])):
            t = threading.Thread(target=animate)
            t.start()
            cmd = True
            details = lookup(sys.argv[1])
            done = True
            sys.stdout.write('\r' + ' ' * 15 + '\r')
            if str(details).upper()[:5] == 'ERROR':
                Exit('fpcalc not found.')
            print("'" + details[1] + "' by " + details[0])
            print(
                "https://www.musicbrainz.org/recording/" + details[2])
        else:
            print('File not found: ' + sys.argv[1])
