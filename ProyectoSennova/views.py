from contextvars import Context
from django.http import HttpResponse
from django.template import Template, Context

def inicio(request):
    return HttpResponse('Vista predterminada :3')

def vistaejemplo(request):
    archivoejemplo = open("ProyectoSennova/Templates/Ejemplo/formulario.html")
    lectura = Template(archivoejemplo.read())
    archivoejemplo.close()
    parametros = Context()
    paginaejemplo = lectura.render(parametros)
    return HttpResponse(paginaejemplo)


def vistapais(request):
    archivopais = open("ProyectoSennova/Templates/PaisCurso/view.html")
    leer = Template(archivopais.read())
    archivopais.close
    parametros = Context()
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)