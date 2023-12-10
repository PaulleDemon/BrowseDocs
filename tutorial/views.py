from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit

from utils.decorators import login_required_rest_api

from docsapp.models import Project

from .models import Tutorial
from .froms import TutorialForm


@login_required
@require_http_methods(['GET', 'POST'])
def create_tutorial_view(request):

    if request.method == 'GET':
        id = request.GET.get('edit')
    
        if id:
            try:
                id = int(id)
                instance = Tutorial.objects.get(id=id)
                return render(request, 'tutorial-create.html', {
                                                                'tutorial': instance
                                                            })

            except (Tutorial.DoesNotExist, ValueError):
                return render(request, '404.html')

        return render(request, 'tutorial-create.html')

    elif request.method == "POST":
        # publish post 
        id = request.GET.get('edit')

        instance = None
        project = None

        if request.POST.get("project"):
            try:
                project = Project.objects.get(unique_id=request.POST.get("project"))

            except Project.DoesNotExist:
                return render(request, 'tutorial-create.html', context={'errors': ["project doesn't exist"], 'tutorial': request.POST})


        if id:
            try:
                id = int(id)
                instance = Tutorial.objects.get(id=id)

            except (Tutorial.DoesNotExist, ValueError):
                return render(request, 'tutorial-create.html', {
                        'errors': ['invalid id']
                    })

            post = request.POST.copy() # to make it mutable
            post['project'] = project

            form = TutorialForm(post, instance=instance)

            if form.is_valid():
                tutorial = form.save(commit=False)
                tutorial.user = request.user
                tutorial.published = True
                tutorial.draft = False
                tutorial.save()

                destination_url = reverse('list-tutorials')
                full_url = f"{destination_url}?my=true"
                return redirect(full_url)

            else:
                # print("errors: ", form.errors)
                return render(request, 'tutorial-create.html', {
                    'errors': form.errors,
                    'tutorial': request.POST
                })


@login_required_rest_api
@require_http_methods(['POST'])
@ratelimit(key='ip', rate='60/min', method=ratelimit.ALL, block=True)
def save_draft(request):

    # id = request.POST.get('id')
    id = request.GET.get('edit')
    instance = None

    if id:
        try:
            id = int(id)
            instance = Tutorial.objects.get(id=id, user=request.user)

        except (Tutorial.DoesNotExist, ValueError):
            return JsonResponse({'error': 'invalid id'}, status=400)

    project = None
    if request.POST.get('project'):
        try:
            project = Project.objects.get(unique_id=request.POST.get('project'))

        except Project.DoesNotExist:
            return JsonResponse({'error': 'invalid project id'})

    post = request.POST.copy() # to make it mutable
    post['project'] = project
    # print("data: ", {**request.POST, 'project': project})
    form = TutorialForm(data=post, instance=instance)


    if form.is_valid():
        tutorial = form.save(commit=False)
        tutorial.user = request.user
        tutorial.published = False
        tutorial.draft = True
        tutorial.save()
        return JsonResponse({'id': tutorial.id}, status=200)

    else:
        # print("errors: ", form.errors)
        return JsonResponse({'error': 'invalid data error'}, status=400)


@require_http_methods(['GET'])
def get_tutorial(request, id, title=None, project_id=None, name=None):

    try:
        tutorial = Tutorial.objects.get(id=id)
        project = None
        
        if project_id:
            
            try:
                project = Project.objects.get(unique_id=project_id)
            except Project.DoesNotExist:
                return render(request, '404.html')

        return render(request, 'tutorial.html', {
                                            'tutorial': tutorial,
                                            'base': project,
                                            'page_title': tutorial.title

                                        })

    except Tutorial.DoesNotExist:
        return render(request, '404.html')


@require_http_methods(['GET'])
def list_tutorials(request, project_id=None, name=None):

    my = request.GET.get('my')

    page_number = request.GET.get("page", 1)

    tutorials = Tutorial.objects.filter(published=True).order_by('-datetime')
    if my == 'true':
        tutorials = Tutorial.objects.filter(user=request.user).order_by('-datetime')

    project = None

    if project_id:

        try:
            project = Project.objects.get(unique_id=project_id)

        except Project.DoesNotExist:
            return render(request, '404.html')

        tutorials = tutorials.filter(project__unique_id=project_id)

    paginator = Paginator(tutorials, per_page=10)
    page = paginator.get_page(page_number)
    return render(request, 'tutorial-list.html', {
                                            'tutorials': page,
                                            'base': project
                                            # 'page': page,
                                            })