import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend

async def mostStarredRepoHandler(username):
    JsonData = {}
    async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
        url = f'https://api.github.com/users/{username}/repos'
        async with session.get(url) as response:
            data = await response.json()
            max_star =0
            mostStarRepo =''
            repo_link = ''
            if(response.status==200):
                for repo in data:
                    star = repo['stargazers_count']
                    if(star>max_star):
                        mostStarRepo = repo['name']
                        repo_link = repo['html_url']
                        max_star = star
                temp = {}
                temp['Repo Name'] = mostStarRepo
                temp['Number of Stars'] = max_star
                temp['Repository Link'] = repo_link
                JsonData['Most Starred Repo'] =temp
                JsonData['Status Code'] = "200"
                return JsonData
            else:
                return {
                    "Message":"Error 404","Status Code":"404"
                }