from django.urls import path

from . import views

app_name = 'geo'
urlpatterns = [
    path('', views.index, name='index'),
    path('crear/', views.push, name='crear'),
    path('listar/', views.list, name='listar'),
    path('borrar/', views.delete, name='borrar'),
    path('geocodificar_base/', views.update, name='geocodificar_base'),
]