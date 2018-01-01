import itertools
import time
import sys
import threading
import acoustID
import search
dots = acoustID.animation
Fin = False


def animation():
    for frame in itertools.cycle(dots):
        if Fin:
            break
        sys.stdout.write('\r'+frame)
        sys.stdout.flush()
        time.sleep(0.2)


t = threading.Thread(target=animation)
t.start()

import stagger
import stagger.id3 as id3
import requests
from bs4 import BeautifulSoup

artist = ''
title = ''

base = 'https://genius.com/'

# need ta figure out how regex works TODO Regex
genius = base+(artist+' '+title+' lyrics').replace(' ', '-').replace("'", '').replace('.', '')


def magic(url):
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
            return magic(search.handle(search.search(artist + ' ' + title)))


lyrics = magic(genius)
Fin = True
sys.stdout.write('\r' + ' ' * 15 + '\r')
print(lyrics)
exit(489)

# TODO Command-line Support
