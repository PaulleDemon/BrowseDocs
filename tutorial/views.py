from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from django_ratelimit.decorators import ratelimit

from utils.decorators import login_required_rest_api

from .models import Tutorial
from .froms import TutorialForm


def create_tutorial_view(request):

    return render(request, 'tutorial-create.html')


@login_required_rest_api
@require_http_methods(['POST'])
@ratelimit(key='ip', rate='60/min', method=ratelimit.ALL, block=True)
def save_draft(request):

    form = TutorialForm(request.POST)

    print("tutorial: ", request.POST.get("body"))
    if form.is_valid():
        tutorial = form.save(commit=False)
        tutorial.user = request.user
        tutorial.save()
        return JsonResponse({'id': tutorial.id}, status=200)

    else:
        print("errors: ", form.errors)
        return JsonResponse({'error': 'invalid data error'}, status=400)


        # except Exception as e:
            # print("exception: ", e)
            # return JsonResponse({'error': 'invalid data error'}, status=400)
