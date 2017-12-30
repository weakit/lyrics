import requests
from bs4 import BeautifulSoup
import threading
import itertools
import time
import sys
import stagger
import stagger.id3 as id3

# TODO optional aid
import acoustID
acoust = acoustID.lookup(acoustID.M101)
artist = acoust[0]
title = acoust[0]

api = '_mqTIAzC6cYLt4QNA4fRO6yLrpnTqPZf2jW5zudjB5-QuczjTj82iK6VNP33SxlZ'
base = 'https://genius.com/'
Fin = False
dots = acoustID.animation


def animation():
    for frame in itertools.cycle(dots):
        if Fin:
            break
        sys.stdout.write('\r'+frame)
        sys.stdout.flush()
        time.sleep(0.2)


t = threading.Thread(target=animation)
t.start()

# need ta figure out how regex works TODO Regex
genius = base+(artist+' '+title+' lyrics').replace(' ', '-').replace("'", '').replace('.', '')


# Haven't found a better way.
def magic(url):
    while True:
        try:
            raw = requests.get(url)
            soup = BeautifulSoup(raw.content, 'html.parser')
            lyrics = soup.find('div', {'class': 'lyrics'}).get_text()
            return lyrics
        except Exception as ex:
            if api == '':
                acoustID.Exit('No Hits.\n'+str(ex))
            else:
                global title, artist
                print('Is the title ' + title + ' and artist ' + artist + ' correct for')
                choice = input('(Y/N)').upper()  # TODO path
                if choice == 'N':
                    artist = input('Enter the Correct Artist:')
                    title = input('Enter the Correct Song Title')
                elif not choice == 'Y':
                    acoustID.Exit('Wrong Choice Mate.')
                search = "https://api.genius.com/search?q=" + artist + ' ' + title
                headers = {'Authorization': 'Bearer ' + api}
                results = requests.get(search, headers=headers)
                return magic(base + results.json()['response']['hits'][0]['result']['path'])


Fin = True
sys.stdout.write('\r' + ' ' * 15 + '\r')
print(magic(genius))
print(genius)

# TODO Command-line Support
