from django.shortcuts import render

def inicio(request):
    return render(request, 'portafolio/inicio.html', {'titulo': 'Inicio', 'nombre': 'Yakin José Esquit Toledo'})

def sobre_mi(request):
    return render(request, 'portafolio/sobre_mi.html', {'titulo': 'Sobre mí'})

def habilidades(request):
    return render(request, 'portafolio/habilidades.html', {'titulo': 'Habilidades'})

def proyectos(request):
    return render(request, 'portafolio/proyectos.html', {'titulo': 'Proyectos'})

def contacto(request):
    return render(request, 'portafolio/contacto.html', {'titulo': 'Contacto'})

def error_404(request, exception=None):
    return render(request, 'portafolio/404.html', {'titulo': 'Página no encontrada'}, status=404)
