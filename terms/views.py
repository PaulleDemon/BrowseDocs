from django.shortcuts import render

from . import models

# Create your views here.
def t_and_c_view(request):

    terms = models.Term.objects.filter(term_type=models.TERM_TYPE.T_AND_C).last()

    return render(request, 'terms.html', {'terms': terms})


def privacy_view(request):
    terms = models.Term.objects.filter(term_type=models.TERM_TYPE.PRIVACY).last()

    return render(request, 'terms.html', {'terms': terms})
