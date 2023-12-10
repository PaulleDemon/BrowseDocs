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

from .models import Blog
from .froms import BlogForm

from docsapp.models import Project


@login_required
@require_http_methods(['GET', 'POST'])
def create_blog_view(request):

    if request.method == 'GET':
        id = request.GET.get('edit')
    
        if id:
            try:
                id = int(id)
                instance = Blog.objects.get(id=id)
                return render(request, 'blog-create.html', {
                                                                'blog': instance
                                                            })

            except (Blog.DoesNotExist, ValueError):
                return render(request, '404.html')

        return render(request, 'blog-create.html')

    elif request.method == "POST":
        # publish post 
        id = request.GET.get('edit')

        instance = None

        try:
            project = Project.objects.get(unique_id=request.POST.get("project"), user=request.user)

        except Project.DoesNotExist:
            return render(request, 'blog-create.html', context={'errors': ["project doesn't exist"], 'blog': request.POST})

        if id:
            try:
                id = int(id)
                instance = Blog.objects.get(id=id)

            except (Blog.DoesNotExist, ValueError):
                
                return render(request, 'blog-create.html', context={'errors': ['invalid id'], 'blog': request.POST})
            

        post = request.POST.copy() # to make it mutable
        post['project'] = project

        form = BlogForm(post, instance=instance)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.published = True
            blog.draft = False
            blog.save()

            destination_url = reverse('list-blogs')
            full_url = f"{destination_url}?my=true"
            return redirect(full_url)

        else:
            # print("errors: ", form.errors)
            return render(request, 'blog-create.html', {
                'errors': form.errors,
                'blog': post
            })


@login_required_rest_api
@require_http_methods(['POST'])
@ratelimit(key='ip', rate='60/min', method=ratelimit.ALL, block=True)
def save_draft(request):

    # id = request.POST.get('id')
    id = request.GET.get('edit')
    instance = None

    try:
        project = Project.objects.get(unique_id=request.POST.get("project"), user=request.user)

    except Project.DoesNotExist:
        return JsonResponse({'error': 'invalid project'}, status=400)

    if id:
        try:
            id = int(id)
            instance = Blog.objects.get(id=id)

        except (Blog.DoesNotExist, ValueError):
            return JsonResponse({'error': 'invalid id'}, status=400)

    post = request.POST.copy() # to make it mutable
    post['project'] = project

    form = BlogForm(post, instance=instance)

    if form.is_valid():
        blog = form.save(commit=False)
        blog.user = request.user
        blog.published = False
        blog.draft = True
        blog.save()
        return JsonResponse({'id': blog.id}, status=200)

    else:
        # print("errors: ", form.errors)
        return JsonResponse({'error': 'invalid data error'}, status=400)


@require_http_methods(['GET'])
def get_blog(request, id, title, project_id):

    try:
        blog = Blog.objects.get(id=id)

        project = None
        
        if project_id:
            
            try:
                project = Project.objects.get(unique_id=project_id)
            except Project.DoesNotExist:
                return render(request, '404.html')

        return render(request, 'blog-view.html', {
                                            'blog': blog,
                                            'base': project,
                                            'page_title': blog.title
                                        })

    except Blog.DoesNotExist:
        return render(request, '404.html')


@require_http_methods(['GET'])
def list_blogs(request, project_id=None, name=None):

    my = request.GET.get('my')

    page_number = request.GET.get("page", 1)

    blogs = Blog.objects.filter(published=True).order_by('-datetime')

    project = None

    if my == 'true':
        blogs = Blog.objects.filter(user=request.user).order_by('-datetime')

    if project_id:

        try:
            project = Project.objects.get(unique_id=project_id)

        except Project.DoesNotExist:
            return render(request, '404.html')

        blogs = blogs.filter(project__unique_id=project_id)

    paginator = Paginator(blogs, per_page=10)
    page = paginator.get_page(page_number)
    return render(request, 'blog-list.html', {
                                                'blogs': page,
                                                'base': project,
                                                'project': project
                                            })