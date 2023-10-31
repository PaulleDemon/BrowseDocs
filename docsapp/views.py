from asgiref.sync import sync_to_async

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


from utils.repos import get_github_repo, read_config_file
from utils.decorators import login_required_for_post, login_required_rest_api



class DocsCreateView(View, LoginRequiredMixin):
    template_name = 'docs-create.html'

    def get(self, request):

        # repos = get_github_repo(request.user.username)

        return render(request, self.template_name, context={
            'repos': [] # repos
        })
    

class ImportRepoView(View, LoginRequiredMixin):

    def post(self, request):

        repo_name = request.POST.get('repo_name') # must be of the format paulledemon/browserdocs
        
        try:
            owner, repo = repo_name.split('/')

        except ValueError:
            return JsonResponse({'repo': 'required repo in the format Owner/Reponame'})

        check_files = read_config_file(owner, repo)

        if isinstance(check_files, dict):

            return JsonResponse({"error": check_files.get('error')})

        return JsonResponse({'success': 'the email has been sent'}, status=200)
