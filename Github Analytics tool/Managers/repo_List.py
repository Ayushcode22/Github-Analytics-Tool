import requests
from aiohttp_client_cache import CachedSession, SQLiteBackend

def repo_List_Handler(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    data = response.json()
    names ={}
    i =1
    for obj in data:
        names[f'Repos{i}']= obj['name']
        i+=1
    return names