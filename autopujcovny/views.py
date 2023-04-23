from django.shortcuts import render
from django.views.generic import DetailView
from .models import Autopujcovna, Hodnoceni, Auto


def index(request):
    context = {
        'nadpis': 'Autopůjčovny ve vašem okolí',
        'autopujcovny': Autopujcovna.objects.all(),
        'hodnoceni': Hodnoceni.objects.order_by('-cas')[:3]
    }
    return render(request, 'index.html', context=context)

# Funkce připravující pohled pro stránku, která zobrazí seznam aut podle typu paliva
def auta_palivo(request, palivo):
    context = {
        'palivo': palivo,
        'auta': Auto.objects.filter(palivo__contains=palivo).order_by('-rok_vyroby'),
    }
    return render(request, 'auto/list.html', context=context)


# Generická třída, která řeší pohled pro zobrazení stránky s detailními informacemi o vybraném autě
class AutoDetailView(DetailView):
    model = Auto
    context_object_name = 'auto'
    template_name = 'auto/detail.html'
