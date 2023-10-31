import json
import base64
import requests


def get_github_repo(username, access_token=None):

    """
        if access token is provided will fetch private repositories as well.
        We'll limit to public repositories
    """

    # Make the API request
    
    if access_token:
        headers = {
'           Authorization': f'token {access_token}',
        }
        response = requests.get('https://api.github.com/user/repos', headers=headers)

    else:
        response = requests.get(f'https://api.github.com/users/{username}/repos')

    repos = []

    if response.status_code == 200:
        repositories = response.json()
        for repo in repositories:
            # Access repository details (e.g., name, description, URL, etc.)
            repos.append(repo)

        return repos

    return False


def check_config_file(owner, repo):

    """
        returns if the repo contains .browsedoc.json or .readthedocs.yaml files
    """

    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents'

    # Send a GET request to retrieve the repository's file list
    response = requests.get(api_url)

    if response.status_code == 200:
        repository_contents = response.json()

        # Check if '.browsedocs.json' is in the repository's top-level
        
        for f in repository_contents:
            if f['name'] == '.browsedocs.json' or f['name'] == '.readthedocs.yaml':
                return f['name']

    return False
    


def read_config_file(owner, repo):
    
    file_path = check_config_file(owner, repo)
    
    if file_path == False:
        return {"error": ".browsedocs.yaml not found"}
    
    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'

    response = requests.get(api_url)

    if response.status_code == 200:
        file_data = response.json()

        # Extract and decode the file content
        if 'content' in file_data:
            file_content = base64.b64decode(file_data['content']).decode('utf-8')
            print(f'Content of {file_path}:\n{file_content}')

            if file_path == '.browsedocs.json':
                try:

                    json.loads(file_content)

                except json.decoder.JSONDecodeError:
                    return {'error': 'error decoding json, check json format'}

            return True

        else:
            return {'error': f'Failed to retrieve content for {file_path}.'}

    elif response.status_code == 404:
        return {"error": ".browsedocs.json not found"}
    
    else:
        return {"error": "An unknown error occurred"}