import itertools
import time
import sys
import threading
from search import handle, search
import stagger
from stagger.id3 import USLT
import requests
import os
from bs4 import BeautifulSoup

dots = ['.   ', '..  ', '... ', ' .. ', '  . ']
Fin = True
printLyrics = False
prefix = ''


def animation():
    for frame in itertools.cycle(dots):
        if Fin:
            time.sleep(0.1)
            continue
        sys.stdout.write(' ' * 16 + '\r' + prefix + frame)
        sys.stdout.flush()
        time.sleep(0.1)


thread = threading.Thread(target=animation)
thread.daemon = True
thread.start()

base = 'https://genius.com/'


def scrape(url):
    """Scrapes Lyrics from URL"""
    while True:
        try:
            raw = requests.get(url)
            soup = BeautifulSoup(raw.content, 'html.parser')
            linguistics = soup.find('div', {'class': 'lyrics'}).get_text()
            return linguistics
        except AttributeError:
            global Fin, got
            Fin = True
            sys.stdout.write('\r')
            return scrape(handle(search(got[0] + ' ' + got[1])))


def read(file):
    global prefix
    prefix = 'Reading ID3 Tags  '
    id3 = stagger.read_tag(file)
    return id3.artist, id3.title


def get(file):
    """Gets the song artist and title from mp3"""
    try:
        import acoustID
    except ModuleNotFoundError:
        return read(file)
    global prefix
    prefix = 'Matching with AcoustID  '
    aid = acoustID.lookup(path)
    if str(aid).upper()[:5] == 'ERROR':
        return read(file)
    return aid[0], aid[1]


def write(file, lyric):
    tags = stagger.read_tag(file)
    tags[USLT] = USLT(lang='eng', desc='Lyrics', text=lyric)
    tags.write(path)


try:
    path = sys.argv[1]
except IndexError:
    print('Usage: lyrical.py path-to-music')
    exit(69)

if os.path.isfile(sys.argv[1]):
    Fin = False
    got = get(path)
    prefix = 'Scraping Lyrics  '
    genius = base+('{0} {1} lyrics'.format(got[0], got[1]).replace(' ', '-').replace("'", '').replace('.', ''))
    # need ta figure out how regex works
    lyrics = scrape(genius)
    prefix = 'Writing Lyrics to file  '
    Fin = True
    write(path, lyrics)
    sys.stdout.write('\r' + ' ' * 15 + '\r' + '\nScraped Lyrics.')
    if printLyrics:
        print('\n\n' + lyrics)
else:
    print(str(path) + ' is not a valid file.')
    exit(420)
