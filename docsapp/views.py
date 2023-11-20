import json

from asgiref.sync import sync_to_async

from django.views import View
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from django_ratelimit.decorators import ratelimit


from .forms import ProjectForm, LinkForm, SponsorForm, SocialForm
from .models import Project, AdditionalLink, Sponsor, Social, SOCIAL, SPONSORS

from utils.repos import get_github_repo, read_config_file, scan_for_doc
from utils.decorators import login_required_for_post, login_required_rest_api


class DocsCreateView(LoginRequiredMixin, View):
    template_name = 'docs-create.html'

    def get(self, request):
        
        step = request.GET.get("step")
        edit = request.GET.get("edit")
        
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

            if edit:
                try:
                    id = int(edit)
                    instance = Project.objects.get(id=id, user=request.user)

                    social = Social.objects.filter(project=instance)
                    sponsor = Sponsor.objects.filter(project=instance)
                    links = AdditionalLink.objects.filter(project=instance)

                    instance.social = {
                       'reddit': social.get(name=SOCIAL.REDDIT).username if social.filter(name=SOCIAL.REDDIT).exists() else '',
                        'discord': social.get(name=SOCIAL.DISCORD).username if social.filter(name=SOCIAL.DISCORD).exists() else '',
                        'mastodon': social.get(name=SOCIAL.MASTODON).username if social.filter(name=SOCIAL.MASTODON).exists() else '',
                        'stackoverflow': social.get(name=SOCIAL.STACKOVERFLOW).username if social.filter(name=SOCIAL.STACKOVERFLOW).exists() else '',
                        'twitter': social.get(name=SOCIAL.TWITTER).username if social.filter(name=SOCIAL.TWITTER).exists() else '',
                    }
                                        

                    instance.sponsor = {
                        'opencollective': sponsor.get(name=SPONSORS.OPEN_COLLECTIVE).username if sponsor.filter(name=SPONSORS.OPEN_COLLECTIVE).exists() else '',
                        'github': sponsor.get(name=SPONSORS.GITHUB).username if sponsor.filter(name=SPONSORS.GITHUB).exists() else '',
                        'patreon': sponsor.get(name=SPONSORS.PATREON).username if sponsor.filter(name=SPONSORS.PATREON).exists() else '',
                        'buymeacoffee': sponsor.get(name=SPONSORS.BUYMEACOFFEE).username if sponsor.filter(name=SPONSORS.BUYMEACOFFEE).exists() else '',
                    }
                    additional_links = []

                    for x in links:
                        additional_links.appned({x.name: x.url})

                    instance.additional_links = additional_links

                    print("instance: ", instance.social)

                    return render(request, 'docs-create.html', {
                        'docs': doc_files.get('docs'),
                        'project': repo,
                        'source': doc_files.get('source'),
                        'config': instance
                    })

                except (Project.DoesNotExist, ValueError):
                    return render(request, '404.html') 

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


        form = ProjectForm(request.POST)

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            social = {
                SOCIAL.REDDIT: request.POST.get('reddit'),
                SOCIAL.STACKOVERFLOW: request.POST.get('stackoverflow'),
                SOCIAL.TWITTER: request.POST.get('twitter'),
                SOCIAL.MASTODON: request.POST.get('mastodon'),
                SOCIAL.DISCORD: request.POST.get('discord'),
            }

            sponsor = {
                SPONSORS.GITHUB: request.POST.get('github'),
                SPONSORS.OPEN_COLLECTIVE: request.POST.get('opencollective'),
                SPONSORS.PATREON: request.POST.get('patreon'),
                SPONSORS.BUYMEACOFFEE: request.POST.get('buymeacoffee'),
            }

            link_name = request.POST.get('link_name') or []
            link_url = request.POST.get('link_url') or []

            print("Link: ", link_name, link_url)

            for key, val in social.items():
                if val:
                    social_form = SocialForm({'project': instance, 'name': key, 'username': val})
                    if social_form.is_valid():
                        social_form.save(commit=True)     

            for key, val in sponsor.items():
                if val:
                    sponsor_form = SponsorForm({'project': instance, 'name': key, 'username': val})
                    if sponsor_form.is_valid():
                        sponsor_form.save(commit=True)     

            for name, link in zip(link_name, link_url):

                if name and link:
                    link_form = LinkForm({'project': instance, 'name': name, 'url': link})

                    if link_form:
                        link_form.save(commit=True)

            destination_url = reverse('list-tutorials')
            full_url = f"{destination_url}?my=true"
            return redirect(full_url)

        else:

            repo_name = request.GET.get("repo_name") # must be of the format paulledemon/browserdocs

            try:
                owner, repo = repo_name.split('/')

            except (ValueError, AttributeError):
                return render(request, '404.html')


            doc_files = scan_for_doc(request.user, owner, repo)
            doc_files['project'] = repo
            doc_files['source'] = f'https://github.com/{repo_name}'
          
            return render(request, self.template_name, context={
                                    'config': doc_files.get('config'),
                                    'docs': doc_files.get('docs'),
                                    'project': repo,
                                    'source': doc_files.get('source'),
                                    'errors': dict(form.errors.items())
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
        exists = Project.objects.filter(unique_name=data.get('name')).exists() and not data.get('name') in ['admin', 'www', 'staff', 'blog']

    else:
        return JsonResponse({'error': 'invalid name'}, status=400)

    return JsonResponse({'exists': exists}, status=200)



@require_http_methods(['GET'])
def project_list(request):

    my = request.GET.get('my')
    page_number = request.GET.get('page', 1)
    projects = Project.objects.all()

    if my == 'true':
        projects = projects.filter(user=request.user)

    paginator = Paginator(projects, per_page=2)
    page = paginator.get_page(page_number)

    return render(request, 'doc-list.html', {
        'projects': page
    })

