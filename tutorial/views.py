from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from django_ratelimit.decorators import ratelimit

from utils.decorators import login_required_rest_api

from .models import Tutorial
from .froms import TutorialForm


def create_tutorial_view(request):

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



def publish_tutorial(request):
    # id = request.POST.get('id')
    id = request.GET.get('edit')

    instance = None

    if id:
        try:
            id = int(id)
            instance = Tutorial.objects.get(id=id)

        except (Tutorial.DoesNotExist, ValueError):
            return render(request, 'tutorial-create.html', {
                    'errors': ['invalid id']
                })

    form = TutorialForm(request.POST, instance=instance)

    if form.is_valid():
        tutorial = form.save(commit=False)
        tutorial.user = request.user
        tutorial.published = True
        tutorial.save()
        return render(request, 'tutorial-create.html')

    else:
        # print("errors: ", form.errors)
        return render(request, 'tutorial-create.html', {
            'errors': form.errors
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
            instance = Tutorial.objects.get(id=id)

        except (Tutorial.DoesNotExist, ValueError):
            return JsonResponse({'error': 'invalid id'}, status=400)

    form = TutorialForm(request.POST, instance=instance)

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

