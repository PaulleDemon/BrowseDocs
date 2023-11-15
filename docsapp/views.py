import json

from asgiref.sync import sync_to_async

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods

from django_ratelimit.decorators import ratelimit

from utils.repos import get_github_repo, read_config_file, scan_for_doc
from utils.decorators import login_required_for_post, login_required_rest_api

from django_firestore.datastructures import CREATE_PROJECT
from django_firestore.utils import ErrorDict, convert_data_to_structure
from django_firestore.database import (project_name_exists, create_or_update_project)

class DocsCreateView(LoginRequiredMixin, View):
    template_name = 'docs-create.html'

    def get(self, request):
        
        step = request.GET.get("step")
        
        if step != '2':
            repos = get_github_repo(request.user)

            return render(request, 'docs-import.html', context={
                            'repos': repos
                        })

        else:
            repo_name = request.GET.get("repo_name") # must be of the format paulledemon/browserdocs

            try:
                owner, repo = repo_name.split('/')

            except (ValueError, AttributeError):
                return JsonResponse({'error': 'required repo in the format Owner/Reponame'}, status=400)


            doc_files = scan_for_doc(request.user, owner, repo)
            doc_files['project'] = repo
            doc_files['source'] = f'https://github.com/{repo_name}'

            # doc_files['config']

            return render(request, 'docs-create.html', context={
                                    'config': doc_files.get('config'),
                                    'docs': doc_files.get('docs'),
                                    'project': repo,
                                    'source': doc_files.get('source')
                                })

    def post(self, request):

        step = request.GET.get("step")
        repo_name = request.GET.get("repo_name") # must be of the format paulledemon/browserdocs

        if step != '2':
            return render(request, '404.html')

        data = dict(request.POST)
      
        instance = create_or_update_project(data)
        print("data: ", instance, isinstance(instance, ErrorDict))


        if isinstance(instance, ErrorDict):

            try:
                owner, repo = repo_name.split('/')

            except (ValueError, AttributeError):
                return JsonResponse({'error': 'required repo in the format Owner/Reponame'}, status=400)


            doc_files = convert_data_to_structure(CREATE_PROJECT, data)

            doc_files['source'] = f'https://github.com/{repo_name}'
            doc_files['project'] = doc_files.get('name')

            print("doc files: ", doc_files)

            return render(request, self.template_name, context={
                                        'config': data,
                                        'docs': doc_files.get('docs'),
                                        'project': repo,
                                        'source': doc_files.get('source'),
                                        'error': [instance.as_dict()]
                                    })

        return render(request, self.template_name, context={
            'data': data
        })




class ImportRepoView(LoginRequiredMixin, View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))

        repo_name = data.get('repo') # must be of the format paulledemon/browserdocs
   
        try:
            owner, repo = repo_name.split('/')

        except (ValueError, AttributeError):
            return JsonResponse({'error': 'required repo in the format Owner/Reponame'}, status=400)

        doc_files = scan_for_doc(request.user, owner, repo)
    
        if doc_files.get('error'):

            return JsonResponse({"error": doc_files.get('error')}, status=400)

        doc_files['project'] = repo
        doc_files['source'] = f'https://github.com/{repo_name}'

        return JsonResponse(doc_files, status=200)


def my_docs(request):
    """
        returns docs that user has created
    """
    

    return render(request, 'mydocs.html', {

    })


def explore_docs(request):

    """
        returns the docs for the user to explore new docs
    """


@login_required_rest_api
@require_http_methods(['POST'])
@ratelimit(key='ip', rate='200/min', method=ratelimit.ALL, block=True)
def check_name_exists(request):
    
    data = json.loads(request.body.decode("utf-8"))

    if data.get('name'):
        exists = project_name_exists(data.get('name')) and not data.get('name') in ['admin', 'www', 'staff', 'blog']

    else:
        return JsonResponse({'error': 'invalid name'}, status=400)

    return JsonResponse({'exists': exists}, status=200)
