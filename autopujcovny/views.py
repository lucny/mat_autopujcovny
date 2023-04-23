from django.shortcuts import render
from .models import Autopujcovna, Hodnoceni


def index(request):
    context = {
        'nadpis': 'Autopůjčovny ve vašem okolí',
        'autopujcovny': Autopujcovna.objects.all(),
        'hodnoceni': Hodnoceni.objects.order_by('-cas')[:3]
    }
    return render(request, 'index.html', context=context)

