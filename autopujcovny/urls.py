from django.urls import path
from . import views
from .views import auta_palivo, AutoDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('auta/palivo/<str:palivo>', auta_palivo, name='auta_list'),
    path('auta/<int:pk>', AutoDetailView.as_view(), name='auta_detail'),
]
