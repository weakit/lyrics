import itertools
import time
import sys
import threading
import stagger
from stagger.id3 import USLT
import requests
import os
from bs4 import BeautifulSoup

api_key = ''

dots = ['.   ', '..  ', '... ', ' .. ', '  . ']
Fin = True
printLyrics = False
prefix = ''
results = 4
aiu = False


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


def search(query):
    if api_key == '':
        return ''
    url = "https://api.genius.com/search?q=" + query
    headers = {'Authorization': 'Bearer ' + api_key}
    hits = requests.get(url, headers=headers)
    return handle(hits.json())


def handle(hits):
    library = {}
    no = 0
    for hit in hits['response']['hits']:
        no += 1
        library[no] = hit['result']['path']
        library[str(no)] = hit['result']['full_title']
        if no == results or no == len(hits['response']['hits']):
            break
    for num in range(int(len(library) / 2)):
        print(str(num + 1) + ': ' + library[str(num + 1)])
    if len(library) == 0:
        choice = input('\nEnter a search query or 1 to quit: ')
    else:
        choice = input('\nChoose an option or enter a search query: ')
    try:
        url = base + library[int(choice)][1:]
        return url
    except (ValueError, KeyError):
        if int(choice) == no + 1:
            exit(8)
        return search(str(choice))


def scrape(url):
    if url == '':
        return ''
    try:
        raw = requests.get(url)
        soup = BeautifulSoup(raw.content, 'html.parser')
        linguistics = soup.find('div', {'class': 'lyrics'}).get_text()
        return linguistics
    except AttributeError:
        global Fin, path, aiu
        Fin = True
        sys.stdout.write('\r')
        if aiu:
            aiu = False
            return scrape(base+('{0} {1} lyrics'.format(read(path)[0], read(path)[1]).replace(' ', '-').replace("'", '').replace('.', '')))
        return scrape(search(read(path)[0] + ' ' + read(path)[1]))


def read(file):
    global prefix
    prefix = 'Reading ID3 Tags  '
    id3 = stagger.read_tag(file)
    return id3.artist, id3.title


def get(file):
    try:
        import acoustID
    except ModuleNotFoundError:
        return read(file)
    global prefix
    prefix = 'Matching with AcoustID  '
    aid = acoustID.lookup(path)
    if str(aid).upper()[:5] == 'ERROR':
        return read(file)
    global aiu
    aiu = True
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

if os.path.isfile(path):
    Fin = False
    got = get(path)
    prefix = 'Scraping Lyrics  '
    genius = base+('{0} {1} lyrics'.format(got[0], got[1]).replace(' ', '-').replace("'", '').replace('.', ''))
    # need ta figure out how regex works
    lyrics = scrape(genius)
    for n in range(2):
        if lyrics == '':
            if n == 1:
                print('Could not find lyrics.')
                exit(16)
            lyrics = scrape(base+('{0} {1} lyrics'.format(read(path)[0], read(path)[1]).replace(' ', '-').replace("'", '').replace('.', '')))
    prefix = 'Writing Lyrics to file  '
    Fin = True
    write(path, lyrics)
    sys.stdout.write('\r' + ' ' * 15 + '\r' + '\nScraped Lyrics.')
    if printLyrics:
        print(lyrics)
else:
    print(str(path) + ' is not a valid file.')
