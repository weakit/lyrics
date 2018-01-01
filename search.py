import requests

api_key = ''  # Genius API Key
base = 'https://genius.com/'
number = 4


def search(query):
    url = "https://api.genius.com/search?q=" + query
    headers = {'Authorization': 'Bearer ' + api_key}
    results = requests.get(url, headers=headers)
    return results.json()


def handle(hits):
    library = {}
    no = 0
    for hit in hits['response']['hits']:
        no += 1
        library[no] = hit['result']['path']
        library[str(no)] = hit['result']['full_title']
        if no == number or no == len(hits['response']['hits']):
            break
    for num in range(int(len(library) / 2)):
        print(str(num + 1) + ': ' + library[str(num + 1)])
    choice = input('\nChoose an option or enter a search query: ')
    try:
        genius = base + library[int(choice)][1:]
        return genius
    except (ValueError, KeyError):
        return handle(search(str(choice)))
