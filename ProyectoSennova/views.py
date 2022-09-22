from cgi import FieldStorage
from distutils.command.upload import upload
from contextvars import Context
from django.http import HttpResponse, JsonResponse
import json
from django.template import Template, Context
from ProyectoSennova.models import Aprendiz, Centro, Convenio, Curso, DepartamentoCurso, Empresa, Ficha, Horas, Jornada, MunicipioCurso, Ocupacion, PaisCurso, ProgramaEspecial, ProgramaFormacion, Regional, Sector
from django.shortcuts import render, redirect
from django.core.files.storage  import FileSystemStorage
from django.contrib import messages
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

#region PAIS CURSO
def viewpais(request):
    pais = PaisCurso.objects.all()
    archivopais = open("ProyectoSennova/Templates/PaisCurso/view.html")
    leer = Template(archivopais.read())
    archivopais.close
    parametros = Context({'pais' : pais})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def insertpais(request):
    if request.method == "POST":
        if request.POST.get('PAISC_Nombre'):
            pais = PaisCurso()
            pais.PAISC_Nombre = request.POST.get('PAISC_Nombre')
            pais.save()
            #insertar = connection.cursor()
            #insertar.execute("call InsertarPaisCurso('"+pais.PAISC_Nombre+"')")
            return redirect('/pais')
    else:
        messages.success(request, "El pais no se guardo correctamente")
        return render(request, 'PaisCurso/insert.html')


def resuljson(request):
    data = list(PaisCurso.objects.values())
    return JsonResponse({'data' : data}, safe=False)


def deletepais(request, id):
    pais = PaisCurso.objects.get(id = id)
    pais.delete()
    return redirect('/pais')

@csrf_exempt
def viewUpdatePais(request, id):
    if request.method == "POST":
        pais = PaisCurso(id = id)
        pais.PAISC_Nombre = request.POST.get('PAISC_Nombre')
        pais.save()
        return redirect('/pais')
    else:
        pais = PaisCurso.objects.get(id = id)
        archivopais = open("ProyectoSennova/Templates/PaisCurso/update.html")
        leer = Template(archivopais.read())
        archivopais.close
        parametros = Context({'pais' : pais})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)


#endregion 


#region DEPARTAMENTO CURSO

def insertDepartamento(request):
    if request.method == "POST":
        if request.POST.get('DEPAR_Nombre'):            
            departamento = DepartamentoCurso(
                DEPAR_Nombre = request.POST['DEPAR_Nombre'],
                paiscurso = PaisCurso.objects.get(id = request.POST['paiscurso'])
                ) 
            departamento.save()
            return redirect('/departamento/')
    else:
        #objetos de pais
        pais = PaisCurso.objects.all()
        parametros = dict({'pais' : pais})
        return render(request, 'DepartamentoCurso/insert.html', parametros)


def viewDepartamento(request):
    departamento = DepartamentoCurso.objects.select_related('paiscurso')
    archivo = open("ProyectoSennova/Templates/DepartamentoCurso/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'departamento' : departamento})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteDepartamento(request, id):
    departamento = DepartamentoCurso.objects.get(id = id)
    departamento.delete()
    return redirect('/departamento')


@csrf_exempt
def viewUpdateDepartamento(request, id):
    if request.method == "POST":
        departamento = DepartamentoCurso(id = id)
        departamento.DEPAR_Nombre = request.POST.get('DEPAR_Nombre')
        departamento.paiscurso = PaisCurso.objects.get(id = request.POST['paiscurso'])

        departamento.save()
        return redirect('/departamento')
    else:
        departamento = DepartamentoCurso.objects.get(id = id)
        pais = PaisCurso.objects.all()
        archivo = open("ProyectoSennova/Templates/DepartamentoCurso/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'departamento' : departamento, 'pais' : pais})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)

#endregion


#region MUNICIPIO CURSO

def insertMunicipio(request):
    if request.method == "POST":
        if request.POST.get('MUNIC_Nombre'):            
            municipio = MunicipioCurso(
                MUNIC_Nombre = request.POST['MUNIC_Nombre'],
                departamentocurso = DepartamentoCurso.objects.get(id = request.POST['departamentocurso'])
                ) 
            municipio.save()
            return redirect('/municipio/')
    else:
        #objetos de departamento
        departamento = DepartamentoCurso.objects.all()
        parametros = dict({'departamento' : departamento})
        return render(request, 'MunicipioCurso/insert.html', parametros)


def viewMunicipio(request):
    municipio = MunicipioCurso.objects.select_related('departamentocurso')
    archivo = open("ProyectoSennova/Templates/MunicipioCurso/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'municipio' : municipio})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteMunicipio(request, id):
    municipio = MunicipioCurso.objects.get(id = id)
    municipio.delete()
    return redirect('/municipio/')


@csrf_exempt
def viewUpdateMunicipio(request, id):
    if request.method == "POST":
        municipio = MunicipioCurso(id = id)
        municipio.MUNIC_Nombre = request.POST.get('MUNIC_Nombre')
        municipio.departamentocurso = DepartamentoCurso.objects.get(id = request.POST['departamentocurso'])

        municipio.save()
        return redirect('/municipio')
    else:
        municipio = MunicipioCurso.objects.get(id = id)
        departamento = DepartamentoCurso.objects.all()
        archivo = open("ProyectoSennova/Templates/MunicipioCurso/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'municipio' : municipio, 'departamento' : departamento})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)

#endregion


#region REGIONAL
def insertRegional(request):
    if request.method == "POST":
        if request.POST.get('REGIO_Nombre'):
            regional = Regional()
            regional.REGIO_Nombre = request.POST.get('REGIO_Nombre')
            regional.save()
            return redirect('/regional')
    else:
        return render(request, 'Regional/insert.html')


def viewRegional(request):
    regional = Regional.objects.all()
    archivo = open("ProyectoSennova/Templates/Regional/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'regional' : regional})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteRegional(request, id):
    regional = Regional.objects.get(id = id)
    regional.delete()
    return redirect('/regional')


@csrf_exempt
def viewUpdateRegional(request, id):
    if request.method == "POST":
        regional = Regional(id = id)
        regional.REGIO_Nombre = request.POST.get('REGIO_Nombre')
        regional.save()
        return redirect('/regional')
    else:
        regional = Regional.objects.get(id = id)
        archivo = open("ProyectoSennova/Templates/Regional/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'regional' : regional})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)


#endregion


#region SECTOR

def insertSector(request):
    if request.method == "POST":
        if request.POST.get('SECTO_Nombre', 'SECTO_Nombre'):
            sector = Sector()
            sector.SECTO_Nombre = request.POST.get('SECTO_Nombre')
            sector.SECTO_NombreNuevo = request.POST.get('SECTO_NombreNuevo')
            sector.save()
            return redirect('/sector')
    else:
        return render(request, 'Sector/insert.html')
 

def viewSector(request):
    sector = Sector.objects.all()
    archivo = open("ProyectoSennova/Templates/Sector/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'sector' : sector})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteSector(request, id):
    sector = Sector.objects.get(id = id)
    sector.delete()
    return redirect('/sector')



@csrf_exempt
def viewUpdateSector(request, id):
    if request.method == "POST":
        sector = Sector(id = id)
        sector.SECTO_Nombre = request.POST.get('SECTO_Nombre')
        sector.SECTO_NombreNuevo = request.POST.get('SECTO_NombreNuevo')
        sector.save()
        return redirect('/sector')
    else:
        sector = Sector.objects.get(id = id)
        archivo = open("ProyectoSennova/Templates/Sector/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'sector' : sector})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)

#endregion


#region JORNADA
def insertJornada(request):
    if request.method == "POST":
        if request.POST.get('JORNA_Nombre'):
            jornada = Jornada()
            jornada.JORNA_Nombre = request.POST.get('JORNA_Nombre')
            jornada.save()
            return redirect('/jornada')
    else:
        return render(request, 'Jornada/insert.html')

def viewJornada(request):
    jornada = Jornada.objects.all()
    archivo = open("ProyectoSennova/Templates/Jornada/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'jornada' : jornada})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteJornada(request, id):
    jornada = Jornada.objects.get(id = id)
    jornada.delete()
    return redirect('/jornada')



@csrf_exempt
def viewUpdateJornada(request, id):
    if request.method == "POST":
        jornada = Jornada(id = id)
        jornada.JORNA_Nombre = request.POST.get('JORNA_Nombre')
        jornada.save()
        return redirect('/jornada')
    else:
        jornada = Jornada.objects.get(id = id)
        archivo = open("ProyectoSennova/Templates/Jornada/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'jornada' : jornada})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)
#endregion


#region EMPRESA

def insertEmpresa(request):
    if request.method == "POST":
        if request.POST.get('EMPRE_Nombre', 'EMPRE_Tipo_Identificacion'):
            empresa = Empresa()
            empresa.EMPRE_Nombre = request.POST.get('EMPRE_Nombre')
            empresa.EMPRE_Identificacion = request.POST.get('EMPRE_Identificacion')
            empresa.EMPRE_Tipo_Identificacion = request.POST.get('EMPRE_Tipo_Identificacion')
            empresa.save()
            return redirect('/empresa')
    else:
        return render(request, 'Empresa/insert.html')

def viewEmpresa(request):
    empresa = Empresa.objects.all()
    archivo = open("ProyectoSennova/Templates/Empresa/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'empresa' : empresa})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteEmpresa(request, id):
    empresa = Empresa.objects.get(id = id)
    empresa.delete()
    return redirect('/empresa')


@csrf_exempt
def viewUpdateEmpresa(request, id):
    if request.method == "POST":
        empresa = Empresa(id = id)
        empresa.EMPRE_Nombre = request.POST.get('EMPRE_Nombre')
        empresa.EMPRE_Identificacion = request.POST.get('EMPRE_Identificacion')
        empresa.EMPRE_Tipo_Identificacion = request.POST.get('EMPRE_Tipo_Identificacion')

        empresa.save()
        return redirect('/empresa')
    else:
        empresa = Empresa.objects.get(id = id)
        archivo = open("ProyectoSennova/Templates/Empresa/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'empresa' : empresa})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)
#endregion


#region CENTRO

def insertCentro(request):
    if request.method == "POST":
        if request.POST.get('CENTR_Nombre', 'regional'):            
            centro = Centro(
                CENTR_Nombre = request.POST['CENTR_Nombre'],
                regional = Regional.objects.get(id = request.POST['regional'])
                ) 
            centro.save()
            return redirect('/centro/')
    else:
        regional = Regional.objects.all()
        parametros = dict({'regional' : regional})
        return render(request, 'Centro/insert.html', parametros)


def viewCentro(request):
    centro = Centro.objects.select_related('regional')
    archivo = open("ProyectoSennova/Templates/Centro/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'centro' : centro})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteCentro(request, id):
    centro = Centro.objects.get(id = id)
    centro.delete()
    return redirect('/centro')


@csrf_exempt
def viewUpdateCentro(request, id):
    if request.method == "POST":
        centro = Centro(id = id)
        centro.CENTR_Nombre = request.POST.get('CENTR_Nombre')
        centro.regional = Regional.objects.get(id = request.POST['regional'])
        centro.save()
        return redirect('/centro')
    else:
        centro = Centro.objects.get(id = id)
        regional = Regional.objects.all()
        archivo = open("ProyectoSennova/Templates/Centro/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'centro' : centro, 'regional' : regional})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)
#endregion


#region OCUPACION

def insertOcupacion(request):
    if request.method == "POST":
        if request.POST.get('OCUPA_Nombre', 'OCUPA_Codigo_Hora'):            
            ocupacion = Ocupacion(
                OCUPA_Nombre = request.POST['OCUPA_Nombre'],
                OCUPA_Codigo_Hora = request.POST['OCUPA_Codigo_Hora'],
                sector = Sector.objects.get(id = request.POST['sector'])
                ) 
            ocupacion.save()
            return redirect('/ocupacion/')
    else:
        sector = Sector.objects.all()
        parametros = dict({'sector' : sector})
        return render(request, 'Ocupacion/insert.html', parametros)


def viewOcupacion(request):
    ocupacion = Ocupacion.objects.select_related('sector')
    archivo = open("ProyectoSennova/Templates/Ocupacion/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'ocupacion' : ocupacion})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteOcupacion(request, id):
    ocupacion = Ocupacion.objects.get(id = id)
    ocupacion.delete()
    return redirect('/ocupacion')


@csrf_exempt
def viewUpdateOcupacion(request, id):
    if request.method == "POST":
        ocupacion = Ocupacion(id = id)
        ocupacion.OCUPA_Nombre = request.POST.get('OCUPA_Nombre')
        ocupacion.OCUPA_Codigo_Hora = request.POST.get('OCUPA_Codigo_Hora')
        ocupacion.sector = Sector.objects.get(id = request.POST['sector'])
        ocupacion.save()
        return redirect('/ocupacion')
    else:
        ocupacion = Ocupacion.objects.get(id = id)
        sector = Sector.objects.all()
        archivo = open("ProyectoSennova/Templates/Ocupacion/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'ocupacion' : ocupacion, 'sector' : sector})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)
#endregion


#region CONVENIO

def insertConvenio(request):
    if request.method == "POST":
        if request.POST.get('CONVE_Nombre'):            
            convenio = Convenio(
                CONVE_Nombre = request.POST['CONVE_Nombre'],
                CONVE_Ampliacion_Cobertura = request.POST['CONVE_Ampliacion_Cobertura'],
                sector = Sector.objects.get(id = request.POST['sector']),
                empresa = Empresa.objects.get(id = request.POST['empresa'])
                ) 
            convenio.save()
            return redirect('/convenio/')
    else:
        sector = Sector.objects.all()
        empresa = Empresa.objects.all()
        parametros = dict({'sector' : sector, 'empresa' : empresa})
        return render(request, 'Convenio/insert.html', parametros)


def viewConvenio(request):
    convenio = Convenio.objects.select_related('sector').select_related('empresa')
    archivo = open("ProyectoSennova/Templates/Convenio/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'convenio' : convenio})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteConvenio(request, id):
    convenio = Convenio.objects.get(id = id)
    convenio.delete()
    return redirect('/convenio')


@csrf_exempt
def viewUpdateConvenio(request, id):
    if request.method == "POST":
        convenio = Convenio(id = id)
        convenio.CONVE_Nombre = request.POST.get('CONVE_Nombre')
        convenio.CONVE_Ampliacion_Cobertura = request.POST.get('CONVE_Ampliacion_Cobertura')
        convenio.sector = Sector.objects.get(id = request.POST['sector'])
        convenio.empresa = Empresa.objects.get(id = request.POST['empresa'])

        convenio.save()
        return redirect('/convenio')
    else:
        convenio = Convenio.objects.get(id = id)
        sector = Sector.objects.all()
        empresa = Empresa.objects.all()
        archivo = open("ProyectoSennova/Templates/Convenio/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'convenio' : convenio, 'sector' : sector, 'empresa' : empresa})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)
#endregion


#region CURSO

def insertCurso(request):
    if request.method == "POST":
        if request.POST.get('CURSO_Numero'):            
            curso = Curso(
                CURSO_Numero = request.POST['CURSO_Numero'],
                CURSO_Nombre = request.POST['CURSO_Nombre'],
                CURSO_Estado = request.POST['CURSO_Estado'],
                CURSO_Tipo = request.POST['CURSO_Tipo'],
                sector = Sector.objects.get(id = request.POST['sector']),
                jornada = Jornada.objects.get(id = request.POST['jornada']),
                municipiocurso = MunicipioCurso.objects.get(id = request.POST['municipiocurso'])
                ) 
            curso.save()
            return redirect('/curso/')
    else:
        sector = Sector.objects.all()
        jornada = Jornada.objects.all()
        municipio = MunicipioCurso.objects.all()
        parametros = dict({'sector' : sector, 'jornada' : jornada, 'municipio' : municipio})
        return render(request, 'Curso/insert.html', parametros)


def viewCurso(request):
    curso = Curso.objects.select_related('sector').select_related('jornada').select_related('municipiocurso')
    archivo = open("ProyectoSennova/Templates/Curso/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'curso' : curso})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteCurso(request, id):
    curso = Curso.objects.get(id = id)
    curso.delete()
    return redirect('/curso')


@csrf_exempt
def viewUpdateCurso(request, id):
    if request.method == "POST":
        curso = Curso(id = id)
        curso.CURSO_Numero = request.POST.get('CURSO_Numero')
        curso.CURSO_Nombre = request.POST.get('CURSO_Nombre')
        curso.CURSO_Estado = request.POST.get('CURSO_Estado')
        curso.CURSO_Tipo = request.POST.get('CURSO_Tipo')
        curso.sector = Sector.objects.get(id = request.POST['sector'])
        curso.jornada = Jornada.objects.get(id = request.POST['jornada'])
        curso.municipiocurso = MunicipioCurso.objects.get(id = request.POST['municipiocurso'])
        curso.save()
        return redirect('/curso')
    else:
        curso = Curso.objects.get(id = id)
        sector = Sector.objects.all()
        jornada = Jornada.objects.all()
        municipiocurso = MunicipioCurso.objects.all()
        archivo = open("ProyectoSennova/Templates/Curso/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'curso' : curso, 'sector' : sector, 'jornada' : jornada, 'municipio' : municipiocurso})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)
#endregion


#region HORAS
def insertHora(request):
    if request.method == "POST":
        if request.POST.get('HORAS_Monitores'):            
            hora = Horas(
                HORAS_Monitores = request.POST['HORAS_Monitores'],
                HORAS_Inst_Empresa = request.POST['HORAS_Inst_Empresa'],
                HORAS_Contratista_Externos = request.POST['HORAS_Contratista_Externos'],
                HORAS_Planta = request.POST['HORAS_Planta'],
                HORAS_Total = request.POST['HORAS_Total'],
                ocupacion = Ocupacion.objects.get(id = request.POST['ocupacion']),
                ) 
            hora.save()
            return redirect('/horas/')
    else:
        ocupacion = Ocupacion.objects.all()
        parametros = dict({'ocupacion' : ocupacion})
        return render(request, 'Horas/insert.html', parametros)


def viewHora(request):
    horas = Horas.objects.select_related('ocupacion')
    archivo = open("ProyectoSennova/Templates/Horas/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'horas' : horas})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteHora(request, id):
    horas = Horas.objects.get(id = id)
    horas.delete()
    return redirect('/horas')


@csrf_exempt
def viewUpdateHoras(request, id):
    if request.method == "POST":
        horas = Horas(id = id)
        horas.HORAS_Monitores = request.POST.get('HORAS_Monitores')
        horas.HORAS_Inst_Empresa = request.POST.get('HORAS_Inst_Empresa')
        horas.HORAS_Contratista_Externos = request.POST.get('HORAS_Contratista_Externos')
        horas.HORAS_Planta = request.POST.get('HORAS_Planta')
        horas.HORAS_Total = request.POST.get('HORAS_Total')
        horas.ocupacion = Ocupacion.objects.get(id = request.POST['ocupacion'])
        horas.save()
        return redirect('/horas')
    else:
        horas = Horas.objects.get(id = id)
        ocupacion = Ocupacion.objects.all()
        archivo = open("ProyectoSennova/Templates/Horas/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'horas' : horas, 'ocupacion' : ocupacion})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)
#endregion


#region PROGRAMA ESPECIAL

def insertProgEsp(request):
    if request.method == "POST":
        if request.POST.get('PROGE_Nombre'):            
            programa = ProgramaEspecial(
                PROGE_Nombre = request.POST['PROGE_Nombre'],
                PROGE_Modalidad = request.POST['PROGE_Modalidad'],
                sector = Sector.objects.get(id = request.POST['sector']),
                ) 
            programa.save()
            return redirect('/programaesp/')
    else:
        sector = Sector.objects.all()
        parametros = dict({'sector' : sector})
        return render(request, 'ProgramaEspecial/insert.html', parametros)


def viewProgEsp(request):
    programa = ProgramaEspecial.objects.select_related('sector')
    archivo = open("ProyectoSennova/Templates/ProgramaEspecial/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'programa' : programa})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteProgEsp(request, id):
    programa = ProgramaEspecial.objects.get(id = id)
    programa.delete()
    return redirect('/programaesp')


@csrf_exempt
def viewUpdateProgEsp(request, id):
    if request.method == "POST":
        programa = ProgramaEspecial(id = id)
        programa.PROGE_Nombre = request.POST.get('PROGE_Nombre')
        programa.PROGE_Modalidad = request.POST.get('PROGE_Modalidad')
        programa.sector = Sector.objects.get(id = request.POST['sector'])
        programa.save()
        return redirect('/programaesp')
    else:
        programa = ProgramaEspecial.objects.get(id = id)
        sector = Sector.objects.all()
        archivo = open("ProyectoSennova/Templates/ProgramaEspecial/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'programa' : programa, 'sector' : sector})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)
#endregion


#region PROGRAMA FORMACION

def insertProgFor(request) :
    if request.method == "POST" and request.FILES['PROGR_URL'] :
            programa = ProgramaFormacion(
                PROGR_Nombre = request.POST['PROGR_Nombre'],
                PROGR_Modalidad = request.POST['PROGR_Modalidad'],
                PROGR_Tipo_Formacion = request.POST['PROGR_Tipo_Formacion'],
                PROGR_Duracion = request.POST['PROGR_Duracion'],
                PROGR_Version = request.POST['PROGR_Version'],
                PROGR_Nivel = request.POST['PROGR_Nivel'],
                PROGR_URL = request.FILES['PROGR_URL'],
                sector = Sector.objects.get(id = request.POST['sector'])
                ) 
           
            #arc =  request.FILES['PROGR_URL']
            #archivo = FileSystemStorage()
            #filename = archivo.save(arc.name, arc)            
            programa.save()
            return redirect('/programafor/')
    else:
        sector = Sector.objects.all()
        parametros = dict({'sector' : sector})
        return render(request, 'ProgramaFormacion/insert.html', parametros)


def viewProgFor(request):
    programa = ProgramaFormacion.objects.select_related('sector')
    archivo = open("ProyectoSennova/Templates/ProgramaFormacion/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'programa' : programa})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteProgFor(request, id):
    programa = ProgramaFormacion.objects.get(id = id)
    programa.delete()
    return redirect('/programafor')


@csrf_exempt
def viewUpdateProgFor(request, id):
    if request.method == "POST":
        programa = ProgramaFormacion(id = id)
        programa.PROGR_Nombre = request.POST.get('PROGR_Nombre')
        programa.PROGR_Modalidad = request.POST.get('PROGR_Modalidad')
        programa.PROGR_Tipo_Formacion = request.POST.get('PROGR_Tipo_Formacion')
        programa.PROGR_Duracion = request.POST.get('PROGR_Duracion')
        programa.PROGR_Version = request.POST.get('PROGR_Version')
        programa.PROGR_Nivel = request.POST.get('PROGR_Nivel')
        programa.PROGR_URL = request.POST.get('PROGR_URL')
        programa.sector = Sector.objects.get(id = request.POST['sector'])
        programa.save()
        return redirect('/programafor')
    else:
        programa = ProgramaFormacion.objects.get(id = id)
        sector = Sector.objects.all()
        archivo = open("ProyectoSennova/Templates/ProgramaFormacion/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'programa' : programa, 'sector' : sector})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)
#endregion


#region FICHA

def insertFicha(request):
    if request.method == "POST":
            ficha = Ficha(
                FICHA_Identificador_Unico = request.POST['FICHA_Identificador_Unico'],
                FICHA_Fecha_Inicio = request.POST['FICHA_Fecha_Inicio'],
                FICHA_Fecha_Terminacion = request.POST['FICHA_Fecha_Terminacion'],
                FICHA_Etapa = request.POST['FICHA_Etapa'],
                FICHA_Nombre_Responsable = request.POST['FICHA_Nombre_Responsable'],
                centro = Centro.objects.get(id = request.POST['centro']),
                programaformacion = ProgramaFormacion.objects.get(id = request.POST['programaformacion']),
                jornada = Jornada.objects.get(id = request.POST['jornada']),
                ) 
            ficha.save()
            return redirect('/ficha/')
    else:
        centro = Centro.objects.all()
        programaformacion = ProgramaFormacion.objects.all()
        jornada = Jornada.objects.all()

        parametros = dict({'centro' : centro, 'programaformacion' : programaformacion, 'jornada' : jornada})
        return render(request, 'Ficha/insert.html', parametros)


def viewFicha(request):
    ficha = Ficha.objects.select_related('jornada').select_related('centro').select_related('programaformacion')
    archivo = open("ProyectoSennova/Templates/Ficha/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'ficha' : ficha})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteFicha(request, id):
    ficha = Ficha.objects.get(id = id)
    ficha.delete()
    return redirect('/ficha')


@csrf_exempt
def viewUpdateFicha(request, id):
    if request.method == "POST":
        ficha = Ficha(id = id)
        ficha.FICHA_Identificador_Unico = request.POST.get('FICHA_Identificador_Unico')
        ficha.FICHA_Fecha_Terminacion = request.POST.get('FICHA_Fecha_Terminacion')
        ficha.FICHA_Fecha_Inicio = request.POST.get('FICHA_Fecha_Inicio')
        ficha.FICHA_Etapa = request.POST.get('FICHA_Etapa')
        ficha.FICHA_Nombre_Responsable = request.POST.get('FICHA_Nombre_Responsable')
        ficha.centro = Centro.objects.get(id = request.POST['centro'])
        ficha.programaformacion = ProgramaFormacion.objects.get(id = request.POST['programaformacion'])
        ficha.jornada = Jornada.objects.get(id = request.POST['jornada'])
        ficha.save()
        return redirect('/ficha')
    else:
        ficha = Ficha.objects.get(id = id)
        centro = Centro.objects.all()
        programaformacion = ProgramaFormacion.objects.all()
        jornada = Jornada.objects.all()
        archivo = open("ProyectoSennova/Templates/Ficha/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'ficha' : ficha, 'centro' : centro, 'programa' : programaformacion, 'jornada' : jornada})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)

#endregion


#region APRENDIZ

def insertAprendiz(request):
    if request.method == "POST":
            aprendiz = Aprendiz(
                APREN_Nombre = request.POST['APREN_Nombre'],
                APREN_Apellido = request.POST['APREN_Apellido'],
                APREN_Documento = request.POST['APREN_Documento'],
                APREN_Tipo_Documento = request.POST['APREN_Tipo_Documento'],
                APREN_Celular = request.POST['APREN_Celular'],
                APREN_Estado = request.POST['APREN_Estado'],
                APREN_Correo = request.POST['APREN_Correo'],
                ficha = Ficha.objects.get(id = request.POST['ficha']),
                ) 
            aprendiz.save()
            return redirect('/aprendiz/')
    else:
        ficha = Ficha.objects.all()
        parametros = dict({'ficha' : ficha})
        return render(request, 'Aprendiz/insert.html', parametros)


def viewAprendiz(request):
    aprendiz = Aprendiz.objects.select_related('ficha')
    archivo = open("ProyectoSennova/Templates/Aprendiz/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'aprendiz' : aprendiz})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


def deleteAprendiz(request, id):
    aprendiz = Aprendiz.objects.get(id = id)
    aprendiz.delete()
    return redirect('/aprendiz')


@csrf_exempt
def viewUpdateAprendiz(request, id):
    if request.method == "POST":
        aprendiz = Aprendiz(id = id)
        aprendiz.APREN_Nombre = request.POST.get('APREN_Nombre')
        aprendiz.APREN_Apellido = request.POST.get('APREN_Apellido')
        aprendiz.APREN_Documento = request.POST.get('APREN_Documento')
        aprendiz.APREN_Tipo_Documento = request.POST.get('APREN_Tipo_Documento')
        aprendiz.APREN_Celular = request.POST.get('APREN_Celular')
        aprendiz.APREN_Estado = request.POST.get('APREN_Estado')
        aprendiz.APREN_Correo = request.POST.get('APREN_Correo')
        aprendiz.ficha = Ficha.objects.get(id = request.POST['ficha'])
        aprendiz.save()
        return redirect('/aprendiz')
    else:
        aprendiz = Aprendiz.objects.get(id = id)
        ficha = Ficha.objects.all()
        archivo = open("ProyectoSennova/Templates/Aprendiz/update.html")
        leer = Template(archivo.read())
        archivo.close
        parametros = Context({'aprendiz' : aprendiz, 'ficha' : ficha})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)

#endregion