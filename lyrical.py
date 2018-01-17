import itertools
import time
import sys
import threading
import acoustID
from search import handle, search
import stagger
from stagger.id3 import USLT
import requests
import os
from bs4 import BeautifulSoup
dots = acoustID.animation
Fin = False
prefix = ''


def animation():
    for frame in itertools.cycle(dots):
        if Fin:
            break
        sys.stdout.write(' ' * 16 + '\r' + prefix + frame)
        sys.stdout.flush()
        time.sleep(0.1)


t = threading.Thread(target=animation)
t.start()

base = 'https://genius.com/'
# need ta figure out how regex works TODO Regex


def Exit(reason):
    print(reason)
    exit(420)


def get(url):
    while True:
        try:
            raw = requests.get(url)
            soup = BeautifulSoup(raw.content, 'html.parser')
            linguistics = soup.find('div', {'class': 'lyrics'}).get_text()
            return linguistics
        except AttributeError:
            global Fin
            Fin = True
            sys.stdout.write('\r')
            return get(handle(search(artist + ' ' + title)))


try:
    path = sys.argv[1]
except IndexError:
    print('Usage: lyrical.py path-to-music')
    exit(69)

if os.path.isfile(sys.argv[1]):
    Fin = True
    prefix = 'Matching with AcoustID  '
    Fin = False
    ID = acoustID.lookup(path)
    tags = stagger.read_tag(path)
    if str(ID).upper()[:5] == 'ERROR':
        print('AcoustID Error: ' + ID[7:] + '\n Using ID3 Tags Instead')
        ID = [tags.artist, tags.title]
    artist = ID[0]
    title = ID[1]
    prefix = 'Scraping Lyrics  '
    genius = base+(artist+' '+title+' lyrics').replace(' ', '-').replace("'", '').replace('.', '')
    lyrics = get(genius)
    Fin = True
    sys.stdout.write('\r' + ' ' * 15 + '\r')
    print(lyrics)
    tags[USLT] = USLT(lang='eng', desc='Genius Lyrics', text=lyrics)
    tags.write(path)
else:
    print(str(path) + ' is not a valid file.')
    exit(420)
