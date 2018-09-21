import os
from freelancersdk.session import Session
from freelancersdk.resources.projects.projects import search_projects
from freelancersdk.resources.projects.helpers import create_search_projects_filter
from freelancersdk.resources.projects.exceptions import ProjectsNotFoundException


url = os.environ.get('FLN_URL')
PATH = os.path.abspath(os.path.dirname(__file__))
token_path = PATH + "/token"
if os.path.exists(token_path):
    token_file = open(token_path, 'r')
    oauth_token = token_file.read()
else:
    oauth_token = os.environ.get('FLN_OAUTH_TOKEN')
if not oauth_token:
    raise Exception("Token not found please create a file 'token' or create env variable 'FLN_OAUTH_TOKEN'")
if url:
    session = Session(oauth_token=oauth_token, url=url)
else:
    session = Session(oauth_token=oauth_token)


def projects_search(query):
    search_filter = create_search_projects_filter(
        sort_field= 'time_updated',
        or_search_query= True,
    )
    try:
        p = search_projects(
            session,
            query=query,
            search_filter=search_filter
        )
    except ProjectsNotFoundException as e:
        print('Error message: {}'.format(e.message))
        print('Server response: {}'.format(e.error_code))
        return None
    else:
        return p


p = projects_search('Logo Design')
if p:
    print('Found projects: {}'.format(p))
