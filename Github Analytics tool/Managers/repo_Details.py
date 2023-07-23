import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend
async def repo_Details_Handler(username,reponame):
    # print("ENTERED ",username,time.ctime())
    JsonData = {}
    async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
        url1 = f"https://api.github.com/repos/{username}/{reponame}"
        async with session.get(url1) as response1:
            if(response1.status==200):
                Data = await response1.json()
                # print(Data)
                JsonData['Name'] = Data['name']
                JsonData['Description'] = Data['description']
                JsonData['Star Count'] = Data['stargazers_count']
                JsonData['Fork Count'] = Data['forks_count']
                JsonData['Language'] = Data['language']
                JsonData['Status Code'] = "200"
                return JsonData
            else:
                return {"Message":"Error","Status Code":"404"}

    

        


                

    









    

    