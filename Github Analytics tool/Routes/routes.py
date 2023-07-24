from sanic import Sanic, Blueprint
from sanic.response import text,json
from sanic_ext import render
from textwrap import dedent
import sys
sys.path.append('/Users/ayush.tripude/Desktop/Github Analytics tool')
from Managers.user_details import user_Details_Handler
from Managers.repo_Details import repo_Details_Handler
from Managers.repo_List import repo_List_Handler
from Managers.sort_repos import handle_sorting
from Managers.most_starred import mostStarredRepoHandler
from Managers.get_language import get_User_Lang
from Managers.get_contributors import repoContributorsHandler
from Managers.get_popular_repository import popular_repository
import asyncio

bp = Blueprint("Ayush")


@bp.get('/')
async def hello(request):
    return text("Hello Ayush")



#CREATE HELP MENU
@bp.get('/help')
async def get_help(request):
    List = [
        " Use route '/user/<username>' to fetch user details ",
        " Use route '/user/<username><reponame>' to fetch details pf particular repository ",
        " Use route '/user/<username>/repos' to fetch names of all repositories of that user ",
        " Use route '/user/<username>/sort?type=<sort_type> for sorting all repositories pf that user ",
        " Use route '/user_comparison for comparing two users. Pass user1 and user2 as query parameters'. ",
        " Use route '/repo_compare' for comparing repositories. Pass user1,repo1,user2,repo2 in request body "
        ]
    return await render(
        "help.html",context = {"Menu":List} ,status=200
    )



# GET USER DETAILS
@bp.get('/user/<username:str>')
async def get_user_details(request,username):
    response = asyncio.get_event_loop().create_task(user_Details_Handler(username))
    response2 = asyncio.get_event_loop().create_task(popular_repository(username))
    await asyncio.gather(*[response,response2],return_exceptions=True)
    response = response.result()
    response2 = response2.result()
    print(response,response2)
    popular_repos = []
    if(response['Status Code']=="200" and response2['Status Code']=="200"):
        print("HERE")
        for i,repo in enumerate(response2['Popular Repos']):
            if(i>1):
                break
            else:
                popular_repos.append(repo[1])
        response['Popular Respositories'] = popular_repos
        return await render (
            "user_details.html",context={"dict":response},status=200
        )
    else:
        return json(response)



#GET REPOSITORY DETAILS FOR A PARTICULAR USER
@bp.get('/user/<username:str>/<reponame:str>')
async def get_repo_details(request,username,reponame):

    task1 = asyncio.get_event_loop().create_task(repo_Details_Handler(username,reponame))
    task2 = asyncio.get_event_loop().create_task(repoContributorsHandler(username,reponame))
    group = asyncio.gather(*[task1,task2],return_exceptions=True)
    await group
    task1 = task1.result()
    task2 = task2.result()

    if(task1['Status Code']=="200" and task2['Status Code']=="200"):
        task1['Contributors'] = task2['List_contributors']
        return await render(
            "repo_details.html",context={"dict":task1},status=200
        )
    else:
        return json(task1)

#GET ALL REPOSITORIES FOR A USER
@bp.get('/user/<username:str>/repos')
async def get_user_repos(request,username):
    response = repo_List_Handler(username)
    return await render(
        "repo_list.html",context={"names":response},status=200
    )

@bp.get('/user/<username:str>/sort')
async def sort_Repos(request,username):
    query_params = request.args
    try:
        sort_type = query_params['type'][0]
    except:
        return json({"Error Message ":" Please use 'type' as parameter of sorting"})
    response = await handle_sorting(username,sort_type)
    if(response['Status Code']=="200"):
        Heading = ["Fork Count","Star Count","Recent Activity","Repository Name"]
        return await render(
            "sort.html",context={"List":response['List'],"headings":Heading},status=200
        )
    elif(response['Status Code']=="404"):
        return json({"Message":response['Message']})
    else:
        return json(response)


@bp.get('/user_comparison')
async def compare_user(request):

    query_params = request.args
    try:
        user1 = query_params['user1'][0]
        user2 = query_params['user2'][0]
    except:
        return json({"Error Message ":" Please use 'user1' and 'user2' for passing username"})
    response1 =asyncio.get_event_loop().create_task( user_Details_Handler(user1))
    response2 =asyncio.get_event_loop().create_task( user_Details_Handler(user2))
    
    user_1_mostStarred = asyncio.get_event_loop().create_task(mostStarredRepoHandler(user1)) 
    user_2_mostStarred = asyncio.get_event_loop().create_task(mostStarredRepoHandler(user2))

    lang_u1 = asyncio.get_event_loop().create_task(get_User_Lang(user1))
    lang_u2 = asyncio.get_event_loop().create_task(get_User_Lang(user2))

    await asyncio.gather(*[response1,response2,user_1_mostStarred,user_2_mostStarred,lang_u1,lang_u2],return_exceptions=True)

    response1 = response1.result()
    response2 = response2.result()
    user_1_mostStarred  = user_1_mostStarred.result()
    user_2_mostStarred = user_2_mostStarred.result()
    lang_u1 = lang_u1.result()
    lang_u2 = lang_u2.result()

    if(response1['Status Code']=='200' and response2['Status Code']=='200' and user_1_mostStarred['Status Code']=='200'and user_2_mostStarred['Status Code']=='200'and lang_u1['Status Code']=='200'and lang_u2['Status Code']=='200'):
        response1['Most Starred Repo'] = user_1_mostStarred['Most Starred Repo']
        response2['Most Starred Repo'] = user_2_mostStarred['Most Starred Repo']
        response1['Languages'] = lang_u1['Languages']
        response2['Languages'] = lang_u2['Languages']
        JsonResp ={}
        JsonResp[response1['Name']]=response1
        JsonResp[response2['Name']]=response2

        headings = []
        content1 = []
        content2 = []
        for key,value in response1.items():
            headings.append(key)
            content1.append(value)
            content2.append(response2[key])

            
        return await render(
            "table.html", context={"heading": headings,"content1":content1,"content2":content2}, status=200
        )
    else:
        return json({"Error Message":"Server Error"})


@bp.post('/repo_compare')
async def comapre_repos(request):
    body = request.json
    try:
        user1 =body['user1']
        user2 = body['user2']
        repo1 = body['repo1']
        repo2 = body['repo2']
    except:
        return json({"Error Message ":" Please use 'user1' and 'user2' for passing username and 'repo1' and 'repo2' for passing repository name"})

    repoDetails1 = asyncio.get_event_loop().create_task( repo_Details_Handler(user1,repo1))

    repoDetails2 = asyncio.get_event_loop().create_task(repo_Details_Handler(user2,repo2))

    group = asyncio.gather(*[repoDetails1,repoDetails2],return_exceptions=True)
    await group

    repoDetails1 = repoDetails1.result()
    repoDetails2 = repoDetails2.result()

    if(repoDetails1['Status Code']=='200' and repoDetails2['Status Code']=='200'):

        headings=["Name","Description","Fork Count","Star Count","Language"]

        return await render(
            "repo_comp.html",context={"repo1":repoDetails1,"repo2":repoDetails2,"heading":headings}, status=200
        ) 
    elif(repoDetails1['Status Code']=='404' or repoDetails2['Status Code']=='404'):
        return json({"Error Message":"Not Found"})
    else:
        return json({"Error Message":"Server Error"})
