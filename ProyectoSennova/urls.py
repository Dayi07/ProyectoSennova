"""ProyectoSennova URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from ProyectoSennova.views import viewUpdatePais, viewpais, insertpais, resuljson, deletepais                                           #PAIS
from ProyectoSennova.views import insertDepartamento, viewDepartamento, deleteDepartamento, viewUpdateDepartamento                      #DEPARTAMENTO
from ProyectoSennova.views import insertRegional, viewRegional, deleteRegional, viewUpdateRegional                                      #REGIONAL
from ProyectoSennova.views import insertSector, viewSector, deleteSector, viewUpdateSector                                              #SECTOR
from ProyectoSennova.views import insertJornada, viewJornada, deleteJornada, viewUpdateJornada                                          #JORNADA
from ProyectoSennova.views import insertEmpresa, viewEmpresa, deleteEmpresa, viewUpdateEmpresa                                          #EMPRESA
from ProyectoSennova.views import insertMunicipio, viewMunicipio, deleteMunicipio, viewUpdateMunicipio                                  #MUNICIPIO
from ProyectoSennova.views import insertCentro, viewCentro, deleteCentro, viewUpdateCentro                                              #CENTRO
from ProyectoSennova.views import insertOcupacion, viewOcupacion, deleteOcupacion, viewUpdateOcupacion                                  #OCUPACION
from ProyectoSennova.views import insertConvenio, viewConvenio, deleteConvenio, viewUpdateConvenio                                      #CONVENIO
from ProyectoSennova.views import insertCurso, viewCurso, deleteCurso, viewUpdateCurso                                                  #CURSO
from ProyectoSennova.views import insertHora, viewHora, deleteHora, viewUpdateHoras                                                     #HORA
from ProyectoSennova.views import insertProgEsp, viewProgEsp, deleteProgEsp, viewUpdateProgEsp                                          #PROGRAMA ESPECIAL
from ProyectoSennova.views import insertProgFor, viewProgFor, deleteProgFor, viewUpdateProgFor, viewUpdateFileProgFor                   #PROGRAMA FORMACION
from ProyectoSennova.views import insertFicha, viewFicha, deleteFicha, viewUpdateFicha                                                  #FICHA
from ProyectoSennova.views import insertAprendiz, viewAprendiz, deleteAprendiz, viewUpdateAprendiz, importarAprendiz                     #APRENDIZ



urlpatterns = [
    path('admin/', admin.site.urls),
    path('pais/', viewpais),
    path('pais/insert/', insertpais),
    path('pais/json/', resuljson, name='jsonpais'),
    path('pais/delete/<int:id>', deletepais, name='deletepais'),
    path('pais/update/<int:id>', viewUpdatePais, name='viewUpdatePais'),

    path('departamento/insert/', insertDepartamento),
    path('departamento/', viewDepartamento),
    path('departamento/delete/<int:id>', deleteDepartamento, name='deleteDepartamento'),
    path('departamento/update/<int:id>', viewUpdateDepartamento, name='updateDepartamento'),

    path('regional/insert', insertRegional),
    path('regional/', viewRegional),
    path('regional/delete/<int:id>', deleteRegional, name='deleteRegional'),
    path('regional/update/<int:id>', viewUpdateRegional, name='updateRegional'),

    path('sector/insert', insertSector),
    path('sector/', viewSector),
    path('sector/delete/<int:id>', deleteSector, name='deleteSector'),
    path('sector/update/<int:id>', viewUpdateSector, name='updateSector'),

    path('jornada', viewJornada),
    path('jornada/insert/', insertJornada),
    path('jornada/delete/<int:id>', deleteJornada, name='deleteJornada'),
    path('jornada/update/<int:id>', viewUpdateJornada, name='updateJornada'),

    path('empresa/insert/', insertEmpresa),
    path('empresa/', viewEmpresa),
    path('empresa/delete/<int:id>', deleteEmpresa, name='deleteEmpresa'),
    path('empresa/update/<int:id>', viewUpdateEmpresa, name='updateEmpresa'),

    path('municipio/insert/', insertMunicipio),
    path('municipio/', viewMunicipio),
    path('municipio/delete/<int:id>', deleteMunicipio, name='deleteMunicipio'),
    path('municipio/update/<int:id>', viewUpdateMunicipio, name='updateMunicipio'),

    path('centro/insert/', insertCentro),
    path('centro/', viewCentro),
    path('centro/delete/<int:id>', deleteCentro, name='deleteCentro'),
    path('centro/update/<int:id>', viewUpdateCentro, name='updateCentro'),

    path('ocupacion/insert/', insertOcupacion),
    path('ocupacion/', viewOcupacion),
    path('ocupacion/delete/<int:id>', deleteOcupacion, name='deleteOcupacion'),
    path('ocupacion/update/<int:id>', viewUpdateOcupacion, name='updateOcupacion'),

    path('convenio/insert/', insertConvenio),
    path('convenio/', viewConvenio),
    path('convenio/delete/<int:id>', deleteConvenio, name='deleteConvenio'),
    path('convenio/update/<int:id>', viewUpdateConvenio, name='updateConvenio'),

    path('curso/insert/', insertCurso),
    path('curso/', viewCurso),
    path('curso/delete/<int:id>', deleteCurso, name='deleteCurso'),
    path('cursos/update/<int:id>', viewUpdateCurso, name='updateCurso'),

    path('horas/insert/', insertHora),
    path('horas/', viewHora),
    path('horas/delete/<int:id>', deleteHora, name='deleteHora'),
    path('horas/update/<int:id>', viewUpdateHoras, name='updateHoras'),

    path('programaesp/insert/', insertProgEsp),
    path('programaesp/', viewProgEsp),
    path('programaesp/delete/<int:id>', deleteProgEsp, name='deleteProgEsp'),
    path('programaesp/update/<int:id>', viewUpdateProgEsp, name='updateProgramaEsp'),

    path('programafor/insert/', insertProgFor),
    path('programafor/', viewProgFor),
    path('programafor/delete/<int:id>', deleteProgFor, name='deleteProgFor'),
    path('programafor/update/<int:id>', viewUpdateProgFor, name='updateProgramaFor'),
    path('programafor/updateFile/<int:id>', viewUpdateFileProgFor, name='UpdateFileProgFor'),


    path('ficha/insert/', insertFicha),
    path('ficha/', viewFicha),
    path('ficha/delete/<int:id>', deleteFicha, name='deleteFicha'),
    path('ficha/update/<int:id>', viewUpdateFicha, name='updateFicha'),

    path('aprendiz/insert/', insertAprendiz),
    path('aprendiz/', viewAprendiz),
    path('aprendiz/delete/<int:id>', deleteAprendiz, name='deleteAprendiz'),
    path('aprendiz/update/<int:id>', viewUpdateAprendiz, name='updateAprendiz'),
    path('aprendiz/import/', importarAprendiz, name='importarAprendiz')

] 


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    