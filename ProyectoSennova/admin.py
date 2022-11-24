from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from .models import Aprendiz, Centro, Contrato, Convenio, Curso, DepartamentoCurso, Empresa, Ficha, Horas, Jornada, MunicipioCurso, Ocupacion, PaisCurso, ProgramaEspecial, ProgramaFormacion, Regional, Sector, User

admin.site.register(User, UserAdmin)
admin.site.register(Permission)

@admin.register(PaisCurso)
class PaisCursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'PAISC_Nombre', ) 
    list_per_page = 20


@admin.register(DepartamentoCurso)
class DepartamentoaAdmin(admin.ModelAdmin):  
    list_display = ('id', 'DEPAR_Nombre', ) 
    list_per_page = 20


@admin.register(MunicipioCurso)
class MunicipioAdmin(admin.ModelAdmin):  
    list_display = ('id', 'MUNIC_Nombre', ) 
    list_per_page = 20


@admin.register(Regional)
class RegionalAdmin(admin.ModelAdmin):  
    list_display = ('id', 'REGIO_Nombre', ) 
    list_per_page = 20


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):  
    list_display = ('id', 'SECTO_Nombre', 'SECTO_NombreNuevo') 
    list_per_page = 20


@admin.register(Jornada)
class JornadaAdmin(admin.ModelAdmin):  
    list_display = ('id', 'JORNA_Nombre',) 
    list_per_page = 20


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):  
    list_display = ('id', 'EMPRE_Nombre') 
    list_per_page = 20


@admin.register(Centro)
class CentroAdmin(admin.ModelAdmin):  
    list_display = ('id', 'CENTR_Nombre') 
    list_per_page = 20


@admin.register(ProgramaFormacion)
class ProgramaFormacionAdmin(admin.ModelAdmin):  
    list_display = ('id', 'PROGR_Nombre') 
    list_per_page = 20


@admin.register(Ficha)
class FichaAdmin(admin.ModelAdmin):     
    list_display = ('id', 'FICHA_Identificador_Unico') 
    list_per_page = 20


@admin.register(Ocupacion)
class OcupacionAdmin(admin.ModelAdmin):  
    list_display = ('id', 'OCUPA_Nombre') 
    list_per_page = 20


@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):  
    list_display = ('id', 'CONVE_Nombre') 
    list_per_page = 20


@admin.register(ProgramaEspecial)
class ProgramaEspecialAdmin(admin.ModelAdmin):  
    list_display = ('id', 'PROGE_Nombre') 
    list_per_page = 20


@admin.register(Horas)
class HorasAdmin(admin.ModelAdmin):  
    list_display = ('id', 'HORAS_Monitores') 
    list_per_page = 20


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):  
    list_display = ('id', 'CURSO_Nombre') 
    list_per_page = 20


@admin.register(Aprendiz)
class AprendizAdmin(admin.ModelAdmin):  
    list_display = ('id', 'APREN_Nombre') 
    list_per_page = 20


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):  
    list_display = ('id', 'CONT_Fecha_Creacion', 'CONT_Estado_Aprendiz', 'CONT_Estado_Contrato') 
    list_per_page = 20




