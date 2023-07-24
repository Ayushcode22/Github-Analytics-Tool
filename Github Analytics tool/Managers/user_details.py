from aiohttp_client_cache import CachedSession, SQLiteBackend

GIT_PATH = "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"

headers = {
        "AUTHENTICATION":f"Bearer{GIT_PATH}"
    }

async def user_Details_Handler(username):

    jsonData={}
    async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
        url = f"https://api.github.com/users/{username}"
        async with session.get(url) as response:
            responseData = await response.json()
            if(response.status==200):
                jsonData['Name'] = responseData['login']
                jsonData['Email'] = responseData['email']
                jsonData['Public Repos'] = responseData['public_repos']
                jsonData['Location'] = responseData['location']
                jsonData['Bio'] = responseData['bio']
                jsonData['User Type'] = responseData['type']
                jsonData['GitHub Profile Link'] = responseData['html_url']
                jsonData['Profile Picture Link'] = responseData['avatar_url']
                jsonData['Followers'] = responseData['followers']
                jsonData['Following'] = responseData['following']
                jsonData['Status Code'] = "200"
                return jsonData
            elif( response.status ==404 and len(responseData)==2 ):
                return {"Error Message": responseData['message'],"Status Code":"404"}
            else:
                return{"Error MEssage":"Server Error","Status Code":"500"}