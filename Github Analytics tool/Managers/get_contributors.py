import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend
async def repoContributorsHandler(username,reponame):
    List_contributors=[]
    JsonResponse = {}
    async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
        url2 = f"https://api.github.com/repos/{username}/{reponame}/contributors"
        async with session.get(url2) as response2:
            if(response2.status==200):
                Data = await response2.json()
                for contrib in Data:
                    temp={}
                    temp[contrib['login']] = contrib['contributions']
                    List_contributors.append(temp)
                JsonResponse['Status Code'] = "200"
                JsonResponse['List_contributors'] = List_contributors
                return JsonResponse
            else:
                return {"Message":"Eror 404","Status Code":"404"}

