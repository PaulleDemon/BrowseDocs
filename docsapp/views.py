import json
from functools import wraps
from urllib.parse import urlparse
from asgiref.sync import sync_to_async

from django.views import View
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from django_ratelimit.decorators import ratelimit

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import  ListModelMixin, CreateModelMixin


from .forms import ProjectForm, LinkForm, SponsorForm, SocialForm
from .models import (Project, AdditionalLink, Sponsor, Social, 
                        Documentation, DocPage,
                        SOCIAL, SPONSORS)

from utils.common import extract_path
from utils.tasks import generate_docs_celery
from utils.throttle import SearchThrottle, UpdateThrottle
from utils.repos import get_github_repo, read_config_file, scan_for_doc
from utils.decorators import login_required_for_post, login_required_rest_api

from .serializers import ProjectSerializer


class ProjectCreateView(LoginRequiredMixin, View):
    template_name = 'project-create.html'

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

            if doc_files.get("error"):
                doc_files['error'] = {'error': [doc_files.get("error")]}

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
                        'paypal': sponsor.get(name=SPONSORS.PAYPAL).username if sponsor.filter(name=SPONSORS.PAYPAL).exists() else '',
                        'buymeacoffee': sponsor.get(name=SPONSORS.BUYMEACOFFEE).username if sponsor.filter(name=SPONSORS.BUYMEACOFFEE).exists() else '',
                    }
                    additional_links = {}

                    for x in links:
                        additional_links.update({x.name: x.url})

                    instance.additional_links = additional_links

                    return render(request, 'project-create.html', {
                        'docs': doc_files.get('docs'),
                        'project': repo,
                        'source': doc_files.get('source'),
                        'config': instance,
                        'update': True
                    })

                except (Project.DoesNotExist, ValueError):
                    return render(request, '404.html') 

            return render(request, 'project-create.html', context={
                                        'config': doc_files.get('config'),
                                        'errors': doc_files.get('error'),
                                        'docs': doc_files.get('docs'),
                                        'project': repo,
                                        'source': doc_files.get('source')
                                })

    def post(self, request):

        step = request.GET.get("step")
        repo_name = request.GET.get("repo_name") # must be of the format paulledemon/browserdocs

        edit = request.GET.get('edit')

        if step != '2':
            return render(request, '404.html')

        instance = None

        try:
            owner, repo = repo_name.split('/')

        except (ValueError, AttributeError):
            return render(request, '404.html')

        if edit:
            try:
                instance = Project.objects.get(id=int(edit), user=request.user)

            except Project.DoesNotExist:
                return render(request, '404.html')

        form = ProjectForm(request.POST, instance=instance)

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            generate_docs_celery(request.user.id, owner, repo, instance.id, request.POST.get("docs"))

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
                SPONSORS.PAYPAL: request.POST.get('paypal'),
            }

            link_name = request.POST.getlist('link_name') or []
            link_url = request.POST.getlist('link_url') or []

            Social.objects.filter(project=instance).delete()
            Sponsor.objects.filter(project=instance).delete()
            AdditionalLink.objects.filter(project=instance).delete()

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

                    if link_form.is_valid():
                        link_form.save(commit=True)

            destination_url = reverse('doc-list')
            full_url = f"{destination_url}?my=true"
            return redirect(full_url)

        else:

            repo_name = request.GET.get("repo_name") # must be of the format paulledemon/browserdocs


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

       
class UpdateDocsView(GenericAPIView):

    throttle_classes = [UpdateThrottle]

    def post(self, request):
        # try:
        project = Project.objects.get(id=int(request.data.get('projectid')), user=request.user)

        generate_docs_celery(request.user.id, project.id)

        # except (Project.DoesNotExist, TypeError):
        #     return Response({'error': 'Permission denied'}, status=403)

        # except Exception as e:
        #     return Response({'error': str(e)}, status=500)

        return Response({'success': 'project is updating'}, status=200)


class DocCreateView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'doc-create.html')

    def post(self, request):

        return render(request, 'doc-create.html')


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


class SearchView(GenericAPIView, ListModelMixin):

    throttle_classes = [SearchThrottle]

    def get_serializer_class(self):

        project = self.request.query_params.get('project')

        if project:
            return ProjectSerializer
        
        return ProjectSerializer
    
    def get_queryset(self):
        project = self.request.query_params.get('project')

        pro_obj = Project.objects.filter(Q(name__istartswith=project)|Q(unique_name__istartswith=project))[:20]
        return pro_obj

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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

    paginator = Paginator(projects.order_by('-datetime'), per_page=20)
    page = paginator.get_page(page_number)

    return render(request, 'doc-list.html', {
        'projects': page
    })




@require_http_methods(['GET'])
def get_docs(request, unique_id, page_url=None, version=None, name=None):

    try:
        project = Project.objects.get(unique_id=unique_id)

        doc = Documentation.objects.filter(project__unique_id=unique_id)

        if not version:
            doc = doc.last()

        else:
            try:
                doc = doc.get(version=version)

            except Documentation.DoesNotExist:
                return render(request, '404.html')

        print("Docs: ", doc)

        doc_page = DocPage.objects.filter(documentation=doc)

        if not page_url:
            doc_page = doc_page.first()

        else:
            try:
                doc_page = doc_page.get(page_url=extract_path(page_url))
                print("page url: ", doc_page)

            except DocPage.DoesNotExist:
                return render(request, '404.html')

        return render(request, 'docs-view.html', {
            'project': project,
            'base': project,
            'doc_page': doc_page,
            'documentation': doc
        })

    except Project.DoesNotExist:
        return render(request, '404.html')
    

@require_http_methods(['GET'])
def get_project_about(request, name, unique_id):
    try:
        project = Project.objects.get(unique_id=unique_id)

        social_obj = Social.objects.filter(project=project)
        sponsor_obj = Sponsor.objects.filter(project=project)

        social = {}
        sponsor = {}

        for x in social_obj:
            if x.name == SOCIAL.DISCORD:
                social[f'https://discord.gg/8xm7PxW4'] = "bi bi-discord"
            
            elif x.name == SOCIAL.REDDIT:
                social[f'https://reddit.com/r/{x.username}'] = "bi bi-reddit"

            elif x.name == SOCIAL.MASTODON:
                social[f'https://mastodon.social/{x.username}'] = "bi bi-mastodon"

            elif x.name == SOCIAL.STACKOVERFLOW:
                social[f'https://stackoverflow.com/questions/tagged/{x.username}'] = "bi bi-stackoverflow"

            elif x.name == SOCIAL.TWITTER:
                social[f'https://twitter.com/{x.username}'] = "bi bi-twitter"

        for x in sponsor_obj:
            if x.name == SPONSORS.GITHUB:
                sponsor[f'https://github.com/sponsors/{x.username}'] = "bi bi-github"
            
            elif x.name == SPONSORS.OPEN_COLLECTIVE:
                sponsor[f'https://opencollective.com/{x.username}'] = "bi bi-opencollective"

            elif x.name == SPONSORS.PATREON:
                sponsor[f'https://www.patreon.com/{x.username}'] = "bi bi-coin"

            elif x.name == SPONSORS.BUYMEACOFFEE:
                sponsor[f'https://buymeacoffee.com/{x.username}'] = "bi bi-coin"
                
            elif x.name == SPONSORS.PAYPAL:
                sponsor[f'https://paypal.me/{x.username}'] = "bi bi-paypal"


        links = AdditionalLink.objects.filter(project=project)

        return render(request, 'docs-about.html', {
            'project': project,
            'base': project,
            'social': social,
            'sponsor': sponsor,
            'links': links
        })

    except Project.DoesNotExist:
        return render(request, '404.html')

