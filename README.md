# lyrical

A program that scrapes lyrics from [Genius](https://www.genius.com) and embeds it into a mp3's ID3 tag.

Requires stagger, BeautifulSoup4 and requests.

To Install these, do
~~~~
pip install stagger requests beautifulsoup4
~~~~

To use the search functionality, you will need an Client Access Token, which you can get at https://genius.com/api-clients. Paste the Token in `lyrical.py`

To use the script, point it to an mp3 file.
~~~~
lyrical.py music.mp3
~~~~

The script also supports identifing mp3s via acoustID.

To do that, place `acoustID.py` alongside the script.
Then you will need to install chromaprint, which you can find [here](https://acoustid.org/chromaprint).

Download the binary and aslo place it alongside the script or in your system path.

If you are on linux, your distribution may have its own package.
