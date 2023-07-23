import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend

async def get_User_Lang(username):
    async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
        url = f'https://api.github.com/users/{username}/repos'
        async with session.get(url) as response:
            if(response.status==200):
                data = await response.json()
                JsonData={}
                languages = list(set([repo['language'] for repo in data if repo['language'] ]))
                JsonData['Languages'] = languages
                JsonData['Status Code'] = "200"
                return JsonData
            else:
                return {
                    "Message":"Error 404","Status Code":"404"
                }
