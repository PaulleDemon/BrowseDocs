from django.shortcuts import render

# Create your views here.

def create_tuotiral_view(request):

    return render(request, 'tutorial-create.html')