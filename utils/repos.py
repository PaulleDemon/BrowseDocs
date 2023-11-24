import json
import base64
import requests

from django.conf import settings
from social_django.models import UserSocialAuth

from user.models import User



def get_headers(user: User):

    try:
        social_auth = UserSocialAuth.objects.get(user=user, provider='github')  # Replace 'github' with the relevant provider
    except UserSocialAuth.DoesNotExist:
        return {
            'User-Agent': 'request',
        }
    

    return {
        'User-Agent': 'request',
        'Authorization': f'Bearer {social_auth.access_token}'
    }

    

def get_github_repo(user: User, access_token=None):

    """
        if access token is provided will fetch private repositories as well.
        We'll limit to public repositories
    """

    # Make the API request
    headers = get_headers(user)

    if access_token:
        # FIXME: nothow I imagined
        headers.update({
'           Authorization': f'token {access_token}',
        })
        response = requests.get('https://api.github.com/user/repos', headers=headers)

    else:
        response = requests.get(f'https://api.github.com/users/{user.username}/repos', headers=headers)

    repos = []

    if response.status_code == 200:
        repositories = response.json()
        # sorts by latest commit
        repos = list(sorted(repositories, key=lambda repo: repo['updated_at'], reverse=True))

    return repos


def check_config_file(user: User, owner, repo):

    """
        returns if the repo contains .browsedoc.json files
    """


    headers = get_headers(user)

    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents'

    # Send a GET request to retrieve the repository's file list
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        repository_contents = response.json()

        # Check if '.browsedocs.json' is in the repository's top-level
        
        for f in repository_contents:
            if f['name'].lower() == '.browsedocs.json': # or f['name'].lower() == '.readthedocs.yaml':
                return f['name']

    return False
    


def read_config_file(user: User, owner, repo) -> dict:
    
    headers = get_headers(user)

    file_path = '.browsedocs.json' #check_config_file(owner, repo)
    
    # if file_path == False:
    #     return {"error": ".browsedocs.yaml not found"}
    
    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        file_data = response.json()

        # Extract and decode the file content
        if 'content' in file_data:
            file_content = base64.b64decode(file_data['content']).decode('utf-8')
            try:
                return json.loads(file_content)

            except json.decoder.JSONDecodeError:
                return {'error': 'error decoding json, check json format of .browsedocs.json'}

        else:
            return {'error': f'Failed to retrieve content for {file_path}.'}

    elif response.status_code == 404:
        return {"error": ".browsedocs.json not found"}
    
    else:
        return {"error": "An unknown error occurred"}


def get_repo_info(user: User, owner, repo):

    headers = get_headers(user)

    repo_url = f'https://api.github.com/repos/{owner}/{repo}'

    response = requests.get(repo_url, headers=headers)

    if response.status_code == 200:
        repo_info = response.json()
        return repo_info



def scan_for_doc(user: User, owner, repo):

    headers = get_headers(user)

    config = read_config_file(user, owner, repo)

    if config.get('error'):
        return config

    path = config.get('source')

    repo_info = get_repo_info(user, owner, repo)

    if not repo_info:
        return {'error': 'repo not found'}

    default_branch = repo_info.get('default_branch')
    # print("defaul branch" , default_branch)
    if not default_branch:
        return {'error': 'repo not found'}

    api = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1'
    # docs_folder_url = f'https://api.github.com/repos/{owner}/{repo}/contents/docs'
    response = requests.get(api, headers=headers)
    docs_names = []

    if response.status_code == 200: 
        contents = response.json()

        for item in contents['tree']:
            
            if item['path'].lower() in ['readme.rst', 'readme.md'] or \
                path and item['path'].lower() == path or \
                item['path'].lower() == 'docs' and item['type'] == 'tree':

                docs_names.append({'path': item['path'], 'type': item['type']}) # only one either readme.rst or readme.md


        if not docs_names:
            return {'error': 'docs couldn\'t be found please modify .browsedocs.json or add docs directory or add readme.md '}

        return {'docs': docs_names, 'config': config}

    elif response.status_code == 404:
        return {'error': 'docs couldn\'t be found please modify .browsedocs.json or add docs directory or add readme.md '}

    

def get_file(user: User, owner, repo, file_path):
    headers = get_headers(user)

    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'
    
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        file_data = response.json()

        # Extract and decode the file content
        if 'content' in file_data:
            file_content = base64.b64decode(file_data['content']).decode('utf-8')
            
            return file_content

        else:
            return {'error': f'Failed to retrieve content for {file_path}.'}
