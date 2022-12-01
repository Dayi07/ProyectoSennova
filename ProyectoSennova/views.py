from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.views.generic import View
from django.contrib.auth.decorators import permission_required, login_required
from sqlalchemy import create_engine
from shutil import rmtree
from xhtml2pdf import pisa
from datetime import date
from contextvars import Context
import pandas as pd   
import re
import os
#from django.contrib.auth.models import User 
from ProyectoSennova.models import Aprendiz, Centro, Contrato, Convenio, Curso, DepartamentoCurso, Empresa, Ficha, Horas, Importar, Jornada, MunicipioCurso, Ocupacion, PaisCurso, ProgramaEspecial, ProgramaFormacion, Regional, Sector, User
from django.template import Template, Context
 




#region PAIS CURSO
@login_required(redirect_field_name='')
def viewpais(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    usuario = request.user
    pais = PaisCurso.objects.all()
    archivopais = open("ProyectoSennova/Templates/PaisCurso/view.html")
    leer = Template(archivopais.read())
    archivopais.close
    parametros = Context({'pais' : pais, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def insertpais(request):
    if request.user.role == 2:
        if request.method == "POST":
            if request.POST.get('PAISC_Nombre'):
                pais = PaisCurso()
                pais.PAISC_Nombre = request.POST.get('PAISC_Nombre')
                pais.save()               
                #insertar = connection.cursor()
                #insertar.execute("call InsertarPaisCurso('"+pais.PAISC_Nombre+"')")
                return redirect('/pais')  
        else:
            usuario = request.user
            messages.success(request, "El pais no se guardo correctamente")
            return render(request, 'PaisCurso/insert.html', {'usuario' : usuario})
    else:
        return redirect('/pais')


def resuljson(request):
    data = list(PaisCurso.objects.values())   
    return JsonResponse({'data' : data})

   
@login_required(redirect_field_name='')
def deletepais(request, id):
    if request.user.role == 2:
        pais = PaisCurso.objects.get(id = id)
        pais.delete()
        return redirect('/pais')
    else:
        return redirect('/pais')


@login_required(redirect_field_name='')
def viewUpdatePais(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            pais = PaisCurso(id = id)
            pais.PAISC_Nombre = request.POST.get('PAISC_Nombre')
            pais.save()
            return redirect('/pais')
        else:
            usuario = request.user
            pais = PaisCurso.objects.get(id = id)
            return render(request, 'PaisCurso/update.html', {'pais' : pais, 'usuario' : usuario})
    else:
        return redirect('/pais')


#endregion 


#region DEPARTAMENTO CURSO
@login_required(redirect_field_name='')
def insertDepartamento(request):
    if request.user.role == 2:
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
            usuario = request.user
            pais = PaisCurso.objects.all()
            return render(request, 'DepartamentoCurso/insert.html', {'pais' : pais, 'usuario' : usuario})
    else:
        return redirect('/departamento/')

    
@login_required(redirect_field_name='')
def viewDepartamento(request):
        if not request.user.is_authenticated:  
            return redirect('/usuario/login')

        departamento = DepartamentoCurso.objects.select_related('paiscurso')
        archivo = open("ProyectoSennova/Templates/DepartamentoCurso/view.html")
        leer = Template(archivo.read())
        archivo.close
        usuario = request.user
        parametros = Context({'departamento' : departamento, 'usuario' : usuario})
        paginalistado = leer.render(parametros)
        return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteDepartamento(request, id):
    if request.user.role == 2:
        departamento = DepartamentoCurso.objects.get(id = id)
        departamento.delete()
        return redirect('/departamento')
    else:
        return redirect('/departamento/')


@login_required(redirect_field_name='')
def viewUpdateDepartamento(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            departamento = DepartamentoCurso(id = id)
            departamento.DEPAR_Nombre = request.POST.get('DEPAR_Nombre')
            departamento.paiscurso = PaisCurso.objects.get(id = request.POST['paiscurso'])

            departamento.save()
            return redirect('/departamento')
        else:
            usuario = request.user
            departamento = DepartamentoCurso.objects.get(id = id)
            pais = PaisCurso.objects.all()
            return render(request, 'DepartamentoCurso/update.html', {'departamento' : departamento, 'pais' : pais, 'usuario' : usuario})
    else:
        return redirect('/departamento/')
    

#endregion


#region MUNICIPIO CURSO

@login_required(redirect_field_name='')
def insertMunicipio(request):
    if request.user.role == 2:
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
            usuario = request.user
            return render(request, 'MunicipioCurso/insert.html', {'departamento' : departamento, 'usuario' : usuario})
    else:
        return redirect('/municipio/')


@login_required(redirect_field_name='')
def viewMunicipio(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    municipio = MunicipioCurso.objects.select_related('departamentocurso')
    archivo = open("ProyectoSennova/Templates/MunicipioCurso/view.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'municipio' : municipio, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteMunicipio(request, id):
    if request.user.role == 2:
        municipio = MunicipioCurso.objects.get(id = id)
        municipio.delete()
        return redirect('/municipio/')
    else:
        return redirect('/municipio')


@login_required(redirect_field_name='')
def viewUpdateMunicipio(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            municipio = MunicipioCurso(id = id)
            municipio.MUNIC_Nombre = request.POST.get('MUNIC_Nombre')
            municipio.departamentocurso = DepartamentoCurso.objects.get(id = request.POST['departamentocurso'])

            municipio.save()
            return redirect('/municipio')
        else:
            usuario = request.user
            municipio = MunicipioCurso.objects.get(id = id)
            departamento = DepartamentoCurso.objects.all()
            return render(request, 'MunicipioCurso/update.html', {'municipio' : municipio, 'departamento' : departamento, 'usuario' : usuario})
    else:
        return redirect('/municipio')
    

#endregion


#region REGIONAL
    
@login_required(redirect_field_name='')
def insertRegional(request):
    if request.user.role == 2:
        if request.method == "POST":
            if request.POST.get('REGIO_Nombre'):
                regional = Regional()
                regional.REGIO_Nombre = request.POST.get('REGIO_Nombre')
                regional.save()
                return redirect('/regional')
        else:
            usuario = request.user
            return render(request, 'Regional/insert.html', {'usuario' : usuario})
    else:
        return redirect('/regional')


@login_required(redirect_field_name='')
def viewRegional(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    regional = Regional.objects.all()
    archivo = open("ProyectoSennova/Templates/Regional/view.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'regional' : regional, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteRegional(request, id):
    if request.user.role == 2:
        regional = Regional.objects.get(id = id)
        regional.delete()
        return redirect('/regional')
    else:
        return redirect('/regional')


@login_required(redirect_field_name='')
def viewUpdateRegional(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            regional = Regional(id = id)
            regional.REGIO_Nombre = request.POST.get('REGIO_Nombre')
            regional.save()
            return redirect('/regional')
        else:
            usuario = request.user
            regional = Regional.objects.get(id = id)
            return render(request, 'Regional/update.html', {'regional' : regional, 'usuario' : usuario})
    else:
        return redirect('/regional')


#endregion


#region SECTOR

@login_required(redirect_field_name='')
def insertSector(request):
    if request.user.role == 2:
        if request.method == "POST":
            if request.POST.get('SECTO_Nombre', 'SECTO_Nombre'):
                sector = Sector()
                sector.SECTO_Nombre = request.POST.get('SECTO_Nombre')
                sector.SECTO_NombreNuevo = request.POST.get('SECTO_NombreNuevo')
                sector.save()
                return redirect('/sector')
        else:
            usuario = request.user
            return render(request, 'Sector/insert.html', {'usuario' : usuario})
    else:
        return redirect('/sector')

@login_required(redirect_field_name='')
def viewSector(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    sector = Sector.objects.all()
    archivo = open("ProyectoSennova/Templates/Sector/view.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'sector' : sector, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteSector(request, id):
    if request.user.role == 2:
        sector = Sector.objects.get(id = id)
        sector.delete()
        return redirect('/sector')
    else:
        return redirect('/sector')

@login_required(redirect_field_name='')
def viewUpdateSector(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            sector = Sector(id = id)
            sector.SECTO_Nombre = request.POST.get('SECTO_Nombre')
            sector.SECTO_NombreNuevo = request.POST.get('SECTO_NombreNuevo')
            sector.save()
            return redirect('/sector')
        else:
            usuario = request.user
            sector = Sector.objects.get(id = id)
            return render(request, 'Sector/update.html', {'sector' : sector, 'usuario' : usuario})
    else:
        return redirect('/sector')

#endregion


#region JORNADA
    
@login_required(redirect_field_name='')
def insertJornada(request):
    if request.user.role == 2:
        if request.method == "POST":
            if request.POST.get('JORNA_Nombre'):
                jornada = Jornada()
                jornada.JORNA_Nombre = request.POST.get('JORNA_Nombre')
                jornada.save()
                return redirect('/jornada')
        else:
            usuario = request.user
            return render(request, 'Jornada/insert.html', {'usuario' : usuario})
    else:
        return redirect('/jornada')

    
@login_required(redirect_field_name='')
def viewJornada(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    jornada = Jornada.objects.all()
    archivo = open("ProyectoSennova/Templates/Jornada/view.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'jornada' : jornada, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteJornada(request, id):
    if request.user.role == 2:
        jornada = Jornada.objects.get(id = id)
        jornada.delete()
        return redirect('/jornada')
    else:
        return redirect('/jornada')


@login_required(redirect_field_name='')
def viewUpdateJornada(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            jornada = Jornada(id = id)
            jornada.JORNA_Nombre = request.POST.get('JORNA_Nombre')
            jornada.save()
            return redirect('/jornada')
        else:
            usuario = request.user
            jornada = Jornada.objects.get(id = id)
            return render(request, 'Jornada/update.html', {'jornada' : jornada, 'usuario' : usuario})
    else:
        return redirect('/jornada')
#endregion


#region EMPRESA
@login_required(redirect_field_name='')
def insertEmpresa(request):
    if request.user.role == 2:
        if request.method == "POST":
            if request.POST.get('EMPRE_Nombre', 'EMPRE_Tipo_Identificacion'):
                empresa = Empresa()
                empresa.EMPRE_Nombre = request.POST.get('EMPRE_Nombre')
                empresa.EMPRE_Identificacion = request.POST.get('EMPRE_Identificacion')
                empresa.EMPRE_Tipo_Identificacion = request.POST.get('EMPRE_Tipo_Identificacion')
                empresa.save()
                return redirect('/empresa') 
        else:
            usuario = request.user
            return render(request, 'Empresa/insert.html', {'usuario' : usuario})
    else:
        return redirect('/empresa')
        
    
@login_required(redirect_field_name='')
def viewEmpresa(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    empresa = Empresa.objects.all()
    usuario = request.user
    archivo = open("ProyectoSennova/Templates/Empresa/view.html")
    leer = Template(archivo.read())
    archivo.close  
    parametros = Context({'empresa' : empresa, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)
  

@login_required(redirect_field_name='')
def deleteEmpresa(request, id):
    if request.user.role == 2:
        empresa = Empresa.objects.get(id = id)
        empresa.delete()
        return redirect('/empresa')
    else:
        return redirect('/empresa')

  
@login_required(redirect_field_name='')
def viewUpdateEmpresa(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            empresa = Empresa(id = id)
            empresa.EMPRE_Nombre = request.POST.get('EMPRE_Nombre')
            empresa.EMPRE_Identificacion = request.POST.get('EMPRE_Identificacion')
            empresa.EMPRE_Tipo_Identificacion = request.POST.get('EMPRE_Tipo_Identificacion')
            empresa.save()
            return redirect('/empresa')
        else:
            usuario = request.user
            empresa = Empresa.objects.get(id = id)
            return render(request, 'Empresa/update.html', {'empresa' : empresa, 'usuario' : usuario})
    else:
        return redirect('/empresa')

      
@login_required(redirect_field_name='')
def viewDetallesEmpresa(request, id):
    empresa = Empresa.objects.get(id = id)
    aprendiz = Contrato.objects.filter(empresa_id = id)
    usuario = request.user
    archivo = open("ProyectoSennova/Templates/Empresa/detalles.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'aprendiz' : aprendiz, 'empresa' : empresa, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)

#endregion


#region CENTRO

@login_required(redirect_field_name='')
def insertCentro(request):
    if request.user.role == 2:
        if request.method == "POST":
            if request.POST.get('CENTR_Nombre', 'regional'):            
                centro = Centro(
                    CENTR_Nombre = request.POST['CENTR_Nombre'],
                    regional = Regional.objects.get(id = request.POST['regional'])
                    ) 
                centro.save()
                return redirect('/centro/')
        else:
            usuario = request.user
            regional = Regional.objects.all()
            return render(request, 'Centro/insert.html', {'regional' : regional, 'usuario' : usuario})
    else:
        return redirect('/centro/')


@login_required(redirect_field_name='')
def viewCentro(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    centro = Centro.objects.select_related('regional')
    usuario = request.user
    archivo = open("ProyectoSennova/Templates/Centro/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'centro' : centro, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteCentro(request, id):   
    if request.user.role == 2:
        centro = Centro.objects.get(id = id)
        centro.delete()
        return redirect('/centro')
    else:
        return redirect('/centro')


@login_required(redirect_field_name='')
def viewUpdateCentro(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            centro = Centro(id = id)
            centro.CENTR_Nombre = request.POST.get('CENTR_Nombre')
            centro.regional = Regional.objects.get(id = request.POST['regional'])
            centro.save()
            return redirect('/centro')
        else:
            usuario = request.user
            centro = Centro.objects.get(id = id)
            regional = Regional.objects.all()
            return render(request, 'Centro/update.html', {'centro' : centro, 'regional' : regional, 'usuario' : usuario})
    else:
        return redirect('/centro')
#endregion


#region OCUPACION

@login_required(redirect_field_name='')
def insertOcupacion(request):
    if request.user.role == 2:
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
            usuario = request.user
            sector = Sector.objects.all()
            return render(request, 'Ocupacion/insert.html', {'sector' : sector, 'usuario' : usuario})
    else:
        return redirect('/ocupacion')


@login_required(redirect_field_name='')
def viewOcupacion(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    ocupacion = Ocupacion.objects.select_related('sector')
    usuario = request.user
    archivo = open("ProyectoSennova/Templates/Ocupacion/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'ocupacion' : ocupacion, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteOcupacion(request, id):
    if request.user.role == 2:
        ocupacion = Ocupacion.objects.get(id = id)
        ocupacion.delete()
        return redirect('/ocupacion')
    else:
        return redirect('/ocupacion')


@login_required(redirect_field_name='')
def viewUpdateOcupacion(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            ocupacion = Ocupacion(id = id)
            ocupacion.OCUPA_Nombre = request.POST.get('OCUPA_Nombre')
            ocupacion.OCUPA_Codigo_Hora = request.POST.get('OCUPA_Codigo_Hora')
            ocupacion.sector = Sector.objects.get(id = request.POST['sector'])
            ocupacion.save()
            return redirect('/ocupacion')
        else:
            usuario = request.user
            ocupacion = Ocupacion.objects.get(id = id)
            sector = Sector.objects.all()
            return render(request, 'Ocupacion/update.html', {'ocupacion' : ocupacion, 'sector' : sector, 'usuario' : usuario})
    else:
        return redirect('/ocupacion')
#endregion


#region CONVENIO

@login_required(redirect_field_name='')
def insertConvenio(request):
    if request.user.role == 2:
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
            usuario = request.user
            sector = Sector.objects.all()
            empresa = Empresa.objects.all()
            return render(request, 'Convenio/insert.html', {'sector' : sector, 'empresa' : empresa, 'usuario' : usuario})
    else:
        return redirect('/convenio')


@login_required(redirect_field_name='')
def viewConvenio(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    convenio = Convenio.objects.select_related('sector').select_related('empresa')
    usuario = request.user
    archivo = open("ProyectoSennova/Templates/Convenio/view.html")
    leer = Template(archivo.read())
    archivo.close
    parametros = Context({'convenio' : convenio, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteConvenio(request, id):
    if request.user.role == 2:
        convenio = Convenio.objects.get(id = id)
        convenio.delete()
        return redirect('/convenio')
    else:
        return redirect('/convenio')


@login_required(redirect_field_name='')
def viewUpdateConvenio(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            convenio = Convenio(id = id)
            convenio.CONVE_Nombre = request.POST.get('CONVE_Nombre')
            convenio.CONVE_Ampliacion_Cobertura = request.POST.get('CONVE_Ampliacion_Cobertura')
            convenio.sector = Sector.objects.get(id = request.POST['sector'])
            convenio.empresa = Empresa.objects.get(id = request.POST['empresa'])

            convenio.save()
            return redirect('/convenio')
        else:
            usuario = request.user
            convenio = Convenio.objects.get(id = id)
            sector = Sector.objects.all()
            empresa = Empresa.objects.all()
            return render(request, 'Convenio/update.html', {'convenio' : convenio, 'sector' : sector, 'empresa' : empresa, 'usuario' : usuario})
    else:
        return redirect('/convenio')
#endregion


#region CURSO

@login_required(redirect_field_name='')
def insertCurso(request):
    if request.user.role == 2:
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
            usuario = request.user
            parametros = dict({'sector' : sector, 'jornada' : jornada, 'municipio' : municipio, 'usuario' : usuario})
            return render(request, 'Curso/insert.html', parametros)
    else:
        return redirect('/curso')


@login_required(redirect_field_name='')
def viewCurso(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    curso = Curso.objects.select_related('sector').select_related('jornada').select_related('municipiocurso')
    archivo = open("ProyectoSennova/Templates/Curso/view.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'curso' : curso, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteCurso(request, id):
    if request.user.role == 2:
        curso = Curso.objects.get(id = id)
        curso.delete()
        return redirect('/curso')
    else:
        return redirect('/curso')

@login_required(redirect_field_name='')
def viewUpdateCurso(request, id):
    if request.user.role == 2:
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
            usuario = request.user
            curso = Curso.objects.get(id = id)
            sector = Sector.objects.all()
            jornada = Jornada.objects.all()
            municipiocurso = MunicipioCurso.objects.all()
            return render(request, 'Curso/update.html', {'curso' : curso, 'sector' : sector, 'jornada' : jornada, 'municipio' : municipiocurso, 'usuario' : usuario})
    else:
        return redirect('/curso')
#endregion


#region HORAS
    
@login_required(redirect_field_name='')
def insertHora(request):
    if request.user.role == 2:
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
            usuario = request.user
            ocupacion = Ocupacion.objects.all()
            parametros = dict({'ocupacion' : ocupacion, 'usuario' : usuario})
            return render(request, 'Horas/insert.html', parametros)
    else:
        return redirect('/horas')


@login_required(redirect_field_name='')
def viewHora(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    horas = Horas.objects.select_related('ocupacion')
    archivo = open("ProyectoSennova/Templates/Horas/view.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'horas' : horas, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteHora(request, id):
    if request.user.role == 2:
        horas = Horas.objects.get(id = id)
        horas.delete()
        return redirect('/horas')
    else:
        return redirect('/hora')


@login_required(redirect_field_name='')
def viewUpdateHoras(request, id):
    if request.user.role == 2:
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
            usuario = request.user
            horas = Horas.objects.get(id = id)
            ocupacion = Ocupacion.objects.all()
            return render(request,'Horas/update.html', {'horas' : horas, 'ocupacion' : ocupacion, 'usuario' : usuario})
    else:
        return redirect('/horas')
#endregion


#region PROGRAMA ESPECIAL

@login_required(redirect_field_name='')
def insertProgEsp(request):
    if request.user.role == 2:
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
            usuario = request.user
            sector = Sector.objects.all()
            parametros = dict({'sector' : sector, 'usuario' : usuario})
            return render(request, 'ProgramaEspecial/insert.html', parametros)
    else:
        return redirect('/programaesp')


@login_required(redirect_field_name='')
def viewProgEsp(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    programa = ProgramaEspecial.objects.select_related('sector')
    archivo = open("ProyectoSennova/Templates/ProgramaEspecial/view.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'programa' : programa, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteProgEsp(request, id):
    if request.user.role == 2:
        programa = ProgramaEspecial.objects.get(id = id)
        programa.delete()
        return redirect('/programaesp')
    else:
        return redirect('/programaesp')


@login_required(redirect_field_name='')
def viewUpdateProgEsp(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            programa = ProgramaEspecial(id = id)
            programa.PROGE_Nombre = request.POST.get('PROGE_Nombre')
            programa.PROGE_Modalidad = request.POST.get('PROGE_Modalidad')
            programa.sector = Sector.objects.get(id = request.POST['sector'])
            programa.save()
            return redirect('/programaesp')
        else:
            usuario = request.user
            programa = ProgramaEspecial.objects.get(id = id)
            sector = Sector.objects.all()
            return render(request, 'ProgramaEspecial/update.html', {'programa' : programa, 'sector' : sector, 'usuario' : usuario})
    else:
        return redirect('/programaesp')
#endregion


#region PROGRAMA FORMACION

@login_required(redirect_field_name='')
def insertProgFor(request) :
    if request.user.role == 2:
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
            usuario = request.user
            sector = Sector.objects.all()
            parametros = dict({'sector' : sector, 'usuario' : usuario})
            return render(request, 'ProgramaFormacion/insert.html', parametros)
    else:
        return redirect('/programafor')


@login_required(redirect_field_name='')
def viewProgFor(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    programa = ProgramaFormacion.objects.select_related('sector')
    archivo = open("ProyectoSennova/Templates/ProgramaFormacion/view.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'programa' : programa, 'usuario' : usuario})
    paginalistado = leer.render(parametros)   
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteProgFor(request, id):
    if request.user.role == 2:
        programa = ProgramaFormacion.objects.get(id = id)
        programa.delete()
        return redirect('/programafor')
    else:
        return redirect('/programafor')


@login_required(redirect_field_name='')
def viewUpdateProgFor(request, id):
    if request.user.role == 2:
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
            usuario = request.user
            programa = ProgramaFormacion.objects.get(id = id)
            sector = Sector.objects.all()
            return render(request, 'ProgramaFormacion/update.html', {'programa' : programa, 'sector' : sector, 'usuario' : usuario})
    else:
        return redirect('/programafor')

    
@login_required(redirect_field_name='')
def viewUpdateFileProgFor(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            programa = ProgramaFormacion(id = id)
            programa.PROGR_Nombre = request.POST.get('PROGR_Nombre')
            programa.PROGR_Modalidad = request.POST.get('PROGR_Modalidad')
            programa.PROGR_Tipo_Formacion = request.POST.get('PROGR_Tipo_Formacion')
            programa.PROGR_Duracion = request.POST.get('PROGR_Duracion')
            programa.PROGR_Version = request.POST.get('PROGR_Version')
            programa.PROGR_Nivel = request.POST.get('PROGR_Nivel')
            programa.PROGR_URL = request.FILES.get('PROGR_URL')
            programa.sector = Sector.objects.get(id = request.POST['sector'])
            programa.save()
            return redirect('/programafor')
        else:
            usuario = request.user
            programa = ProgramaFormacion.objects.get(id = id) 
            sector = Sector.objects.all()
            return render(request, 'ProgramaFormacion/updateFile.html', {'programa' : programa, 'sector' : sector, 'usuario' : usuario})
    else:
        return redirect('/programafor')

    
@login_required(redirect_field_name='')
def viewDetallesProgFor(request, id):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    programa = ProgramaFormacion.objects.get(id = id)
    ficha = Ficha.objects.filter(programaformacion = programa.id)
    usuario = request.user
    
    total_ficha = len(ficha)

    archivo = open("ProyectoSennova/Templates/ProgramaFormacion/detalles.html")
    leer = Template(archivo.read())
    archivo.close

    #Se envian las variables a la vista
    parametros = Context({'programa' : programa, 'ficha' : ficha, 'total_ficha' : total_ficha, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)

#endregion


#region FICHA

@login_required(redirect_field_name='')
def insertFicha(request):
    if request.user.role == 2:
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
                    FICHA_Actualizacion_Carga = date.today()
                    ) 
                ficha.save()
                return redirect('/ficha/')
        else:
            centro = Centro.objects.all()
            programaformacion = ProgramaFormacion.objects.all()
            jornada = Jornada.objects.all()
            usuario = request.user
            parametros = dict({'centro' : centro, 'programaformacion' : programaformacion, 'jornada' : jornada, 'usuario' : usuario})
            return render(request, 'Ficha/insert.html', parametros)
    else:
        return redirect('/ficha')


@login_required(redirect_field_name='')
def viewFicha(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    ficha = Ficha.objects.select_related('jornada').select_related('centro').select_related('programaformacion')
    archivo = open("ProyectoSennova/Templates/Ficha/view.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'ficha' : ficha, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteFicha(request, id):
    if request.user.role == 2:
        ficha = Ficha.objects.get(id = id)
        ficha.delete()
        return redirect('/ficha')
    else:
        return redirect('/ficha')


@login_required(redirect_field_name='')
def viewUpdateFicha(request, id):
    if request.user.role == 2:
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
            ficha.FICHA_Actualizacion_Carga = date.today()
            ficha.save()
            return redirect('/ficha')
        else:
            usuario = request.user
            ficha = Ficha.objects.get(id = id)
            centro = Centro.objects.all()
            programaformacion = ProgramaFormacion.objects.all()
            jornada = Jornada.objects.all()
            return render(request, 'Ficha/update.html', {'ficha' : ficha, 'centro' : centro, 'programa' : programaformacion, 'jornada' : jornada, 'usuario' : usuario})
    else:
        return redirect('/ficha')
    

@login_required(redirect_field_name='')
def viewDetallesFicha(request, id):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    ficha = Ficha.objects.get(id = id)
    aprendiz = Aprendiz.objects.filter(ficha = ficha.id)
    usuario = request.user
    
    #Se calcula el total de los aprendices 
    total_apre = len(aprendiz)

    #Se crean dos listas para guardar los aprendices con y sin contrato
    lista_contra = []
    lista_ncon = []
    lista_term = []


    #Se recorren los aprendices asociados a la ficha seleccionada
    for i in Aprendiz.objects.filter(ficha = ficha.id):  

        if  Contrato.objects.filter(aprendiz = i.id):
            contrato = Contrato.objects.filter(aprendiz = i.id)            

            for n in contrato:
                #Separamos los Aprendices sin contrato
                if n.CONT_Estado_Aprendiz.strip() != 'Contratado' and n.CONT_Estado_Aprendiz.strip() != 'Final Contrato':
                    lista_ncon.append(n)

                #Separamos los Aprendices con contrato
                if n.CONT_Estado_Aprendiz.strip() == 'Contratado':
                    lista_contra.append(n)  

                #Separamos los Aprendices con contrato finalizado
                if n.CONT_Estado_Aprendiz.strip() == 'Final Contrato':
                    lista_term.append(n)  
  

    archivo = open("ProyectoSennova/Templates/Ficha/detalles.html")
    leer = Template(archivo.read())
    archivo.close

    labels = ['Contratado', 'Disponible', 'Terminado']
    data = [len(lista_contra), len(lista_ncon), len(lista_term)]

    #Se envian las variables a la vista
    parametros = Context({'ficha' : ficha, 'aprendiz' : aprendiz, 'contrato' : lista_contra, 'total_apre' : total_apre, 'sinContrato' : lista_ncon, 'terminado' : lista_term, 'data' : data, 'labels' : labels, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


#endregion


#region APRENDIZ

@login_required(redirect_field_name='')
def insertAprendiz(request):
    if request.user.role == 2:
        if request.method == "POST" and request.FILES['APREN_Foto']:
                aprendiz = Aprendiz(
                    APREN_Nombre = request.POST['APREN_Nombre'],
                    APREN_Apellido = request.POST['APREN_Apellido'],
                    APREN_Documento = request.POST['APREN_Documento'],
                    APREN_Tipo_Documento = request.POST['APREN_Tipo_Documento'],
                    APREN_Celular = request.POST['APREN_Celular'],
                    APREN_Estado = request.POST['APREN_Estado'],
                    APREN_Correo = request.POST['APREN_Correo'],
                    APREN_Foto = request.FILES['APREN_Foto'],
                    ficha = Ficha.objects.get(id = request.POST['ficha']),
                    )  
                aprendiz.save()
                return redirect('/aprendiz/')
        else:
            usuario = request.user
            ficha = Ficha.objects.all()
            parametros = dict({'ficha' : ficha, 'usuario' : usuario})
            return render(request, 'Aprendiz/insert.html', parametros)
    else:
        return redirect('/aprendiz')


@login_required(redirect_field_name='')
def viewAprendiz(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    aprendiz = Aprendiz.objects.select_related('ficha')
    archivo = open("ProyectoSennova/Templates/Aprendiz/view.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'aprendiz' : aprendiz, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteAprendiz(request, id):
    if request.user.role == 2:
        aprendiz = Aprendiz.objects.get(id = id)
        aprendiz.delete()
        return redirect('/aprendiz')
    else:
        return redirect('/aprendiz')


@login_required(redirect_field_name='')
def viewUpdateAprendiz(request, id):
    if request.user.role == 2:
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
            aprendiz.APREN_Foto = request.POST.get('APREN_Foto')
            aprendiz.save()
            return redirect('/aprendiz')
        else:
            usuario = request.user
            aprendiz = Aprendiz.objects.get(id = id)
            ficha = Ficha.objects.all()
            return render(request, 'Aprendiz/update.html', {'aprendiz' : aprendiz, 'ficha' : ficha, 'usuario' : usuario})
    else:
        return redirect('/aprendiz')


@login_required(redirect_field_name='')
def updateFotoAprendiz(request, id):
    if request.user.role == 2:
        if request.method == "POST" and request.FILES['APREN_Foto']:
            aprendiz = Aprendiz(id = id)
            aprendiz.APREN_Nombre = request.POST.get('APREN_Nombre')
            aprendiz.APREN_Apellido = request.POST.get('APREN_Apellido')
            aprendiz.APREN_Documento = request.POST.get('APREN_Documento')
            aprendiz.APREN_Tipo_Documento = request.POST.get('APREN_Tipo_Documento')
            aprendiz.APREN_Celular = request.POST.get('APREN_Celular')
            aprendiz.APREN_Estado = request.POST.get('APREN_Estado')
            aprendiz.APREN_Correo = request.POST.get('APREN_Correo')
            aprendiz.APREN_Foto = request.FILES.get('APREN_Foto')
            aprendiz.ficha = Ficha.objects.get(id = request.POST['ficha'])
            aprendiz.save()
            return redirect('/aprendiz/detalles/'+ str(id))
        else:
            usuario = request.user
            aprendiz = Aprendiz.objects.get(id = id)
            ficha = Ficha.objects.all()
            return render(request, 'Aprendiz/updateFoto.html', {'aprendiz' : aprendiz, 'ficha' : ficha, 'usuario' : usuario})
    else:
        return redirect('/aprendiz')


@login_required(redirect_field_name='')
def importarAprendiz(request):
    if request.user.role == 2:
        #Se guarda el archivo para su lectura
        if request.method == "POST" :
            doc = Importar()
            doc.importar = request.FILES.get('importar')
            doc.save()

            #Se crea la URL de lectura con el nombre del archivo
            archivo = str(doc.importar)
            url = 'http://127.0.0.1:8000/media/'+archivo

            #Se crea el engine(motor) con las especificaiones de la Base de Datos
            engine = create_engine('mysql://root@localhost/ProyectoEtapa')

            #Se hace una lectura de prueba para verificar el numero de columnas y con eso verificar que el documento sea el correcto
            prueba = pd.read_excel(io = url, sheet_name=0, header=4)
            columnas =  len(prueba.columns)   
            if columnas == 7:
                pass
            else:
                mensaje = 'El documento no es el correcto. Por favor verifique y vuelva a intentarlo.'
                return render(request, 'aprendiz/import.html', {'mensaje' : mensaje})


            try:
                #Se hacen dos lecturas del documento excel
                #Uno con el documento completo para la captura de la Ficha
                datos = pd.read_excel(io = url, sheet_name=0, names=['APREN_Tipo_Documento', 'APREN_Documento', 'APREN_Nombre', 'APREN_Apellido', 'APREN_Celular', 'APREN_Correo', 'APREN_Estado'], index_col=None).fillna(value='Por definir')

                #Otra con solo los datos de la tabla 
                datos2 = pd.read_excel(io = url, sheet_name=0, header=4, names=['APREN_Tipo_Documento', 'APREN_Documento', 'APREN_Nombre', 'APREN_Apellido', 'APREN_Celular', 'APREN_Correo', 'APREN_Estado'], index_col=None).fillna(value='Por definir')

                #Se hace la busqueda de la Ficha y se usa split para separar las demas palabras
                busq = datos.loc[0,'APREN_Nombre']
                busq.split()
                ficha = re.split(r'\s+', busq)


                #Se busca en la clase la Ficha capturada si ya esta registrada se captura, si no esta registrada se guarda
                if Ficha.objects.filter(FICHA_Identificador_Unico = ficha[0]):
                    ficha_def = Ficha.objects.get(FICHA_Identificador_Unico = ficha[0])
                else:
                    new_ficha = Ficha(
                        FICHA_Identificador_Unico = ficha[0],
                        FICHA_Fecha_Inicio = date.today(),
                        FICHA_Fecha_Terminacion = date.today(),
                        FICHA_Actualizacion_Carga = date.today(),
                        FICHA_Etapa = 'Por definir',
                        FICHA_Nombre_Responsable = 'Por definir',
                        jornada = Jornada(id = 1),
                        programaformacion = ProgramaFormacion(id = 1),
                        centro = Centro(id = 1)
                    )
                    new_ficha.save()
                    ficha_def = new_ficha

                #Se guarda la fecha de Actualizacion en la ficha
                ficha_def.FICHA_Actualizacion_Carga = date.today()
                ficha_def.save()

                #Se inserta una nueva columna con el Id de la Ficha
                datos2.insert(7, "ficha_id", ficha_def.id, allow_duplicates=False)

                #Se crea una lista para almacenar los indices con datos duplicados (Que ya estan en la Base de Datos)            
                lista = []
                for i in range(0, len(datos2)):
                    #Se recorre la columna del Documento
                    num = datos2.iloc[i]['APREN_Documento']

                    #Buscamos el estado del Aprendiz en el documento
                    est = datos2.loc[i, 'APREN_Estado']
                    cor = datos2.loc[i, 'APREN_Correo']
                    cel = datos2.loc[i, 'APREN_Celular']
                    #Se busca si esta en la Base de Datos
                    if Aprendiz.objects.filter(APREN_Documento = num):
                        aprendiz = Aprendiz.objects.get(APREN_Documento = num)
                        lista.append(i)
                        
                        #Comparamos el estado del aprendiz, lo guardamos en caso de que sea diferente y se agrega el indice a la lista 
                        if aprendiz.APREN_Estado != est:
                            aprendiz.APREN_Estado = est
                            aprendiz.save()
                        
                        if aprendiz.APREN_Correo != cor:
                            aprendiz.APREN_Correo = cor
                            aprendiz.save()
                        if aprendiz.APREN_Celular != cel:
                            aprendiz.APREN_Celular = cel
                            aprendiz.save()        

                #Se borran las filas por medio de sus indices y se guarda en un nuevo DataFrame
                datos_completos = datos2.drop(lista, axis=0)
                
                #Se borra la carpeta donde se encuentra el Excel debido a que ya hizo la lectura
                rmtree("ProyectoSennova/media/Importar")  
                #Se guardan los datos del DataFrame en la Base de Datos          
                datos_completos.to_sql(name = 'Aprendiz', con = engine, if_exists = 'append', index=False)
            except:
                return redirect('/aprendiz')

        else:
            usuario = request.user
            return render(request, 'aprendiz/import.html', {'usuario' : usuario})
    else:
        return redirect('/aprendiz')


@login_required(redirect_field_name='')
def viewDetallesAprendiz(request, id):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    aprendiz = Aprendiz.objects.get(id = id)
    contrato = Contrato.objects.filter(aprendiz = aprendiz.id)
    verificar = contrato.exists()
    usuario = request.user
    
    archivo = open("ProyectoSennova/Templates/Aprendiz/detalles.html")
    leer = Template(archivo.read())
    archivo.close

    #Se envian las variables a la vista   
    parametros = Context({'aprendiz' : aprendiz, 'contrato' : contrato, 'verificar' : verificar, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


#endregion 


#region CONTRATO
@login_required(redirect_field_name='')
def insertContrato(request):
    if request.user.role == 2:
        if request.method == "POST":
            contrato = Contrato(
                CONT_Fecha_Creacion = request.POST['CONT_Fecha_Creacion'],
                CONT_Fecha_Inicio = request.POST['CONT_Fecha_Inicio'],
                CONT_Fecha_Terminacion = request.POST['CONT_Fecha_Terminacion'],
                CONT_Estado_Aprendiz = request.POST['CONT_Estado_Aprendiz'],
                CONT_Estado_Contrato = request.POST['CONT_Estado_Contrato'],
                aprendiz = Aprendiz.objects.get(id = request.POST['aprendiz']),
                empresa = Empresa.objects.get(id = request.POST['empresa']),
                )
            contrato.save()
            return redirect('/contrato/')
        else:
            usuario = request.user
            aprendiz = Aprendiz.objects.all()
            empresa = Empresa.objects.all()
            parametros = dict({'aprendiz' : aprendiz, 'empresa' : empresa, 'usuario' : usuario})
            return render(request, 'Contrato/insert.html', parametros)
    else:
        return redirect('/contrato')


@login_required(redirect_field_name='')
def viewContrato(request):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    contrato = Contrato.objects.select_related('empresa').select_related('aprendiz')
    archivo = open("ProyectoSennova/Templates/Contrato/view.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'contrato' : contrato, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)


@login_required(redirect_field_name='')
def deleteContrato(request, id):
    if request.user.role == 2:
        contrato = Contrato.objects.get(id = id)
        contrato.delete()
        return redirect('/contrato')
    else:
        return redirect('/contrato')


@login_required(redirect_field_name='')
def viewUpdateContrato(request, id):
    if request.user.role == 2:
        if request.method == "POST":
            contrato = Contrato(id = id)
            contrato.CONT_Fecha_Creacion = request.POST['CONT_Fecha_Creacion']
            contrato.CONT_Fecha_Inicio = request.POST['CONT_Fecha_Inicio']
            contrato.CONT_Fecha_Terminacion = request.POST['CONT_Fecha_Terminacion']
            contrato.CONT_Estado_Aprendiz = request.POST['CONT_Estado_Aprendiz']
            contrato.CONT_Estado_Contrato = request.POST['CONT_Estado_Contrato']
            contrato.aprendiz = Aprendiz.objects.get(id = request.POST['aprendiz'])
            contrato.empresa = Empresa.objects.get(id = request.POST['empresa'])
            contrato.save()
            return redirect('/contrato') 
        else:
            contrato = Contrato.objects.get(id = id)
            aprendiz = Aprendiz.objects.all()
            empresa = Empresa.objects.all()
            usuario = request.user
            return render(request, 'Contrato/update.html', {'contrato' : contrato, 'aprendiz' : aprendiz, 'empresa' : empresa, 'usuario' : usuario})
    else:
        return redirect('/contrato')


@login_required(redirect_field_name='')
def importarContrato(request):
    if request.user.role == 2:
        if request.method == "POST" :
            #Se guarda el documento para su lectura
            doc = Importar()
            doc.importar = request.FILES.get('importar')
            doc.save()

            #Creamos la url de la ubicacion del archivo con su nombre
            archivo = str(doc.importar)
            url = 'http://127.0.0.1:8000/media/'+archivo

            #Se crea el motor
            engine = create_engine('mysql://root@localhost/ProyectoEtapa')

            #Se hace una lectura de prueba para verificar el numero de columnas y con eso verificar que el documento sea el correcto
            prueba = pd.read_excel(io = url, sheet_name=0, header=4)
            columnas =  len(prueba.columns)   
            if columnas == 22:
                pass
            else:
                mensaje = 'El documento no es el correcto. Por favor verifique y vuelva a intentarlo.'
                return render(request, 'aprendiz/import.html', {'mensaje' : mensaje})

            try:

                #Se hace la lectura del documento y se eliminan las columnas que no se necesitan 
                datos = pd.read_excel(io = url,  sheet_name=0, header=0, names=['TIPODOCUMENTO', 'APREN_Documento', 'APELLIDOS', 'NOMBRES', 'DIRECCION', 'CIUDAD', 'CONT_Estado_Aprendiz', 'MOTIVO', 'FECHA1','FICHA', 'CODIGO', 'CENTRO', 'ESPECIALIDAD', 'FECHA2', 'FECHA3', 'REGIONAL', 'CONT_Fecha_Creacion', 'NIT', 'EMPRESA', 'CONT_Fecha_inicio', 'CONT_Fecha_Terminacion', 'CONT_Estado_Contrato'], parse_dates=['CONT_Fecha_Creacion', 'CONT_Fecha_inicio', 'CONT_Fecha_Terminacion'], index_col=None)
                datos2 = datos.drop(['TIPODOCUMENTO', 'APELLIDOS', 'NOMBRES', 'DIRECCION', 'CIUDAD', 'MOTIVO', 'FECHA1', 'CODIGO', 'CENTRO', 'ESPECIALIDAD', 'FECHA2', 'FECHA3', 'REGIONAL', 'NIT', 'EMPRESA'], axis=1).fillna(value='vacio')

                #Se añaden las columnas de las foraneas
                datos2.insert(7, "aprendiz_id", 1, allow_duplicates=True)
                datos2.insert(8, "empresa_id", 1, allow_duplicates=True)
                
                #Se crea una lista para guradr el indice de los datos que ya estan guardados
                lista = []
                
                for i in range(0, len(datos2)):
                    
                    #Buscamos algunos datos para su posterios comparacion
                    busq_ficha = datos2.loc[i,'FICHA']
                    num = datos2.iloc[i]['APREN_Documento']  
                    busq_empresa = datos.loc[i, 'NIT']
                    est_aprendiz = datos2.loc[i, 'CONT_Estado_Aprendiz']
                    est_contrato = datos2.loc[i, 'CONT_Estado_Contrato']
                    fec_inicio = datos2.loc[i, 'CONT_Fecha_inicio']
                    fec_final = datos2.loc[i, 'CONT_Fecha_Terminacion']


                    #Verificamos si tiene un estado de Aprendiz diferente para guardar los datos faltantes
                    if est_aprendiz.strip() != 'Contratado' and est_aprendiz.strip() != 'Final Contrato':
                        datos2.loc[i, 'CONT_Estado_Contrato'] = 'SIN CONTRATO'
                        datos2.loc[i, 'CONT_Fecha_inicio'] = date.today()
                        datos2.loc[i, 'CONT_Fecha_Terminacion'] = date.today()

                    #Buscamos la ficha en la base y la creamos en caso de que no este
                    if Ficha.objects.filter(FICHA_Identificador_Unico = busq_ficha):
                        ficha_busq = Ficha.objects.get(FICHA_Identificador_Unico = busq_ficha)
                    else:
                        new_ficha = Ficha(
                            FICHA_Identificador_Unico = busq_ficha,
                            FICHA_Fecha_Inicio = date.today(),
                            FICHA_Fecha_Terminacion = date.today(),
                            FICHA_Actualizacion_Carga = date.today(),
                            FICHA_Etapa = 'Por definir',
                            FICHA_Nombre_Responsable = 'Por definir',
                            jornada = Jornada(id = 1),
                            programaformacion = ProgramaFormacion(id = 1),
                            centro = Centro(id = 1)                             #Los ID de las claves foreanes son hechas desde la base de datos 
                        )
                        new_ficha.save()

                    #Buscamos si ya existe la empresa y se guarda si ID en el Excel
                    if Empresa.objects.filter(EMPRE_Identificacion = busq_empresa):
                        empresa = Empresa.objects.get(EMPRE_Identificacion = busq_empresa)
                        datos2.loc[i, 'empresa_id'] = empresa.id
                    else:
                        #Si no encuentra la empresa crea una
                        empresa = Empresa(
                            EMPRE_Tipo_Identificacion = 'NIT',
                            EMPRE_Nombre = datos.loc[i, 'EMPRESA'],
                            EMPRE_Identificacion = datos.loc[i, 'NIT']
                        )
                        empresa.save()
                        datos2.loc[i, 'empresa_id'] = empresa.id



                    #Buscamos el aprendiz en la base de datos
                    if Aprendiz.objects.filter(APREN_Documento = num):
                        aprendiz = Aprendiz.objects.get(APREN_Documento = num)
                        datos2.loc[i,'aprendiz_id'] = aprendiz.id

                        #Buscamos si ya existe un contrato asociado a ese aprendiz
                        if Contrato.objects.filter(aprendiz = aprendiz.id):
                            for u in Contrato.objects.filter(aprendiz = aprendiz.id):
                                #contrato = Contrato.objects.get(aprendiz = aprendiz.id)
                                lista.append(i)

                                #Se comparan todos los datos y si hay algun cambio se actualiza
                                if u.CONT_Estado_Aprendiz != est_aprendiz:
                                    u.CONT_Estado_Aprendiz = est_aprendiz
                                    u.save() 

                                if u.CONT_Estado_Contrato != est_contrato and est_contrato != 'vacio':
                                    u.CONT_Estado_Contrato = est_contrato
                                    u.save()  

                                if u.CONT_Fecha_Inicio != fec_inicio and fec_inicio != 'vacio':
                                    u.CONT_Fecha_Inicio = fec_inicio
                                    u.save()

                                if u.CONT_Fecha_Terminacion != fec_final and fec_final != 'vacio': 
                                    u.CONT_Fecha_Terminacion = fec_final
                                    u.save()    

                                if u.empresa.EMPRE_Identificacion != busq_empresa:
                                    u.empresa = Empresa.objects.get(EMPRE_Identificacion = busq_empresa)
                                    u.save()
                    else:
                        #Si no encuentra el Aprendiz se crea uno con los datos del Excel
                        aprendiz = Aprendiz(
                            APREN_Nombre = datos.loc[i, 'NOMBRES'],
                            APREN_Apellido = datos.loc[i, 'APELLIDOS'],
                            APREN_Documento = datos.loc[i, 'APREN_Documento'],
                            APREN_Tipo_Documento = datos.loc[i, 'TIPODOCUMENTO'],
                            APREN_Celular = 'Por definir',
                            APREN_Estado = 'Por definir',
                            APREN_Correo = 'Por definir',
                            APREN_Foto = 'Aprendiz/user.jpg',
                            ficha = Ficha.objects.get(FICHA_Identificador_Unico = busq_ficha)
                        )
                        aprendiz.save()                         
                        datos2.loc[i,'aprendiz_id'] = aprendiz.id

                #Eliminamos las columnas que ya no sirven
                datos3 = datos2.drop(['APREN_Documento', 'FICHA'], axis=1)

                #Eliminamos las filas con los datos que ya estan registrados
                datos_completos = datos3.drop(lista, axis=0)
                
                #Eliminamos la carpeta donde se almacenan los archivos
                rmtree("ProyectoSennova/media/Importar")  

                #Se gurdan los datos en la Base de datos        
                datos_completos.to_sql(name = 'Contrato', con = engine, if_exists = 'append', index=False)
            except:
                return redirect('/contrato')
        else:
            #Se retorna una vista
            usuario = request.user
            return render(request, 'contrato/import.html', {'usuario' : usuario})
    else:
        return redirect('/contrato')

    
@login_required(redirect_field_name='')
def viewDetallesContrato(request, id):
    if not request.user.is_authenticated:  
        return redirect('/usuario/login')

    contrato = Contrato.objects.get(id = id)
    aprendiz = Aprendiz.objects.get(APREN_Documento = contrato.aprendiz.APREN_Documento)
    usuario = request.user
    
    archivo = open("ProyectoSennova/Templates/Contrato/detalles.html")
    leer = Template(archivo.read())
    archivo.close

    #Se envian las variables a la vista
    parametros = Context({'aprendiz' : aprendiz, 'contrato' : contrato, 'usuario' : usuario})
    paginalistado = leer.render(parametros)
    return HttpResponse(paginalistado)

#endregion


#region USUARIO

#Ejemplo de Vista basada en Clase
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Usuario/index.html')

    

def insertUsuario(request):
    if request.method == "POST":
        user = User.objects.create_user(
            request.POST.get('username'),
            request.POST.get('email'),
            request.POST.get('password')
        )
        user.last_name = request.POST['last_name']
        user.first_name = request.POST['first_name']
        user.role = 1
        user.save() 
        
        login(request, user)
        return redirect('/index')  
    else:
        return render(request, "Usuario/insert.html")


def loginUsuario(request):   
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('/index')      
        else:
            mensaje = 'Usuario o contraseña incorrecta'
            return render(request, 'Usuario/login.html', {'mensaje' : mensaje})
    else:
        return render(request, 'Usuario/login.html')


def logoutUsuario(request):
    logout(request)
    return redirect('/accounts/login')


def viewIndex(request):
    archivo = open("ProyectoSennova/Templates/Usuario/index.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'usuario' : usuario})
    paginalistado = leer.render(parametros) 
    return HttpResponse(paginalistado)


def viewPerfil(request):
    archivo = open("ProyectoSennova/Templates/Usuario/perfil.html")
    leer = Template(archivo.read())
    archivo.close
    usuario = request.user
    parametros = Context({'usuario' : usuario})
    paginalistado = leer.render(parametros) 
    return HttpResponse(paginalistado)

      
def updateFotoUsuario(request, id):
    if request.method == "POST" and request.FILES['foto']:
        usuario = request.user
        usuario.foto = request.FILES.get('foto')
        usuario.save()
        return redirect('/perfil')
    else:
        usuario = request.user
        return render(request, 'Usuario/updateFoto.html', {'usuario' : usuario})
    

#endregion


#region REPORTE

def reporteFicha(request, id):
    template_path = 'Ficha/reporte.html'

    ficha = Ficha.objects.get(id = id)
    aprendiz = Aprendiz.objects.filter(ficha = ficha.id)
    fecha = date.today()

    lista_contra = []
    lista_ncon = []
    lista_term = []

    #Se recorren los aprendices asociados a la ficha seleccionada
    for i in Aprendiz.objects.filter(ficha = ficha.id):  

        if  Contrato.objects.filter(aprendiz = i.id):
            contrato = Contrato.objects.get(aprendiz = i.id)            

                #Separamos los Aprendices sin contrato
            if contrato.CONT_Estado_Aprendiz.strip() != 'Contratado' and contrato.CONT_Estado_Aprendiz.strip() != 'Final Contrato':
                lista_ncon.append(contrato)

                #Separamos los Aprendices con contrato
            if contrato.CONT_Estado_Aprendiz.strip() == 'Contratado' :
                lista_contra.append(contrato)  

            if contrato.CONT_Estado_Aprendiz.strip() == 'Final Contrato':
                lista_term.append(contrato)  

    parametros = {'ficha' : ficha, 'aprendiz' : aprendiz, 'contrato' : lista_contra,'sinContrato' : lista_ncon, 'terminado' : lista_term, 'fecha' : fecha}
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachmen; filename="Reporte de Aprendices Ficha.pdf"'
    template = get_template(template_path)
    html = template.render(parametros)
    pisa_estatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisa_estatus.err:
        return HttpResponse("Error al cargar el reporte", html)
    return response


def link_callback(uri, rel):
    result = finders.find(uri)
    if result:
            if not isinstance(result, (list, tuple)):
                    result = [result] 
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
    else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/
            if uri.startswith(mUrl):
                    path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                    path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                    return uri
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

#endregion




