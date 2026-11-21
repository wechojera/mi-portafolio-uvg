from django.urls import path
from . import views

app_name = 'portafolio'
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('sobre-mi/', views.sobre_mi, name='sobre_mi'),
    path('habilidades/', views.habilidades, name='habilidades'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('contacto/', views.contacto, name='contacto'),
    path('404/', views.error_404, name='error_404'),
]
