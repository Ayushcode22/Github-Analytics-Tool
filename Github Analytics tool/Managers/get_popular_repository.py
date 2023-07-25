import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend


async def popular_repository(username):
    popular_repos=[]

    async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
        url = f'https://api.github.com/users/{username}/repos'
        async with session.get(url) as response:
            if (response.status==200):
                print("here")
                JsonResponse={}
                data = await response.json()
                for repo in data:
                    popular_repos.append([repo['forks_count']+repo['stargazers_count'],repo['name']])
                popular_repos.sort(key=lambda popular_repos:popular_repos[0],reverse=True)
                JsonResponse['Popular Repos'] = popular_repos
                JsonResponse['Status Code'] = "200"
                print(JsonResponse)
                return JsonResponse
            else:
                return {"Message":"Error","Status Code":"404"}
    