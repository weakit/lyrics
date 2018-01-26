# lyrical

A program that scrapes lyrics from [Genius](https://www.genius.com) and embeds it into a mp3's ID3 tag.

Requires stagger, BeautifulSoup4 and requests

To Install these, do
~~~~
pip install stagger requests beautifulsoup4
~~~~

To use the search functionality, you will need an Client Access Token, which you can get at https://genius.com/api-clients. Paste the Token in `search.py`

The script also supports identifing mp3s via acoustID.

To do that, place the `acoustID.py` file alongside `search.py` and `lyrical.py`.
Then you will need to install chromaprint, which you can find [here](https://acoustid.org/chromaprint).
Download the binary and place it alongside the script.
