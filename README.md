# lyrics-scraper

A python script that scrapes lyrics from [Genius](https://www.genius.com) and embeds it into a mp3's ID3 tag.

Requires stagger, BeautifulSoup4 and requests.

To Install these, do
~~~~
pip install stagger requests beautifulsoup4
~~~~

To use the search functionality, you will need an Client Access Token, which you can get at https://genius.com/api-clients. Paste the Token in `lyrical.py`

To use the script, download `lyrical.py` and point it towards an mp3 file.
~~~~
lyrical.py music.mp3
~~~~
## AcoustID Identification

If you have a bunch of mp3s with incorrect information or have feature artists in the artist/title tag, the script will (mostly) fail to find the lyrics.
To fix this, the script also supports identifing music via [acoustID](https://acoustid.org).

To use acoustID, place `acoustID.py` alongside the script.

Then you will need to install chromaprint, which you can find [here](https://acoustid.org/chromaprint).
Download the binary and aslo place it alongside the script or in your system path.

If you are on linux, your distribution may have its own package.
