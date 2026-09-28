from django.urls import path

from . import views

urlpatterns = [
    # Resuelve a /api/v1/comprar/  (el prefijo api/v1/ viene del urls.py raiz)
    path('comprar/', views.comprar, name='comprar'),
]
