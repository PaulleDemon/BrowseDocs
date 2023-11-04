import json

from asgiref.sync import sync_to_async

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


from utils.repos import get_github_repo, read_config_file, scan_for_doc
from utils.decorators import login_required_for_post, login_required_rest_api



class DocsCreateView(View, LoginRequiredMixin):
    template_name = 'docs-create.html'

    def get(self, request):

        repos = get_github_repo(request.user)
      
        return render(request, self.template_name, context={
            'repos': repos
        })
    

class ImportRepoView(View, LoginRequiredMixin):

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

        return JsonResponse(doc_files, status=200)
