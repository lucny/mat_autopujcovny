from django.contrib import admin
from .models import Autopujcovna, Auto, Zakaznik, Hodnoceni, Pronajem

admin.site.register(Autopujcovna)
admin.site.register(Auto)
admin.site.register(Zakaznik)
admin.site.register(Hodnoceni)
admin.site.register(Pronajem)