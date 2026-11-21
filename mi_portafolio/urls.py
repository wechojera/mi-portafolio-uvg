from django.urls import include, path

urlpatterns = [path('', include('portafolio.urls'))]
handler404 = 'portafolio.views.error_404'
