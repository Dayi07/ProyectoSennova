from pyexpat import model
from tkinter import CASCADE
from django.db import connection
from django.db import models


class PaisCurso(models.Model):
    PAISC_Nombre = models.CharField(max_length=50) 
    class Meta:
        db_table = 'Pais_Curso'



class DepartamentoCurso(models.Model):
    DEPAR_Nombre = models.CharField(max_length=50)
    paiscurso = models.ForeignKey(
        PaisCurso, 
        on_delete=models.CASCADE, 
        )  
    class Meta:
        db_table = 'Departamento_Curso'



class MunicipioCurso(models.Model):
    MUNIC_Nombre = models.CharField(max_length=50)
    departamentocurso = models.ForeignKey(
        DepartamentoCurso,
        on_delete = models.CASCADE,
    )
    class Meta:
        db_table = 'Municipio_Curso'



class Regional(models.Model):
    REGIO_Nombre = models.CharField(max_length=50)
    class Meta:
        db_table = 'Regional'



class Sector(models.Model):
    SECTO_Nombre = models.CharField(max_length=50)
    SECTO_NombreNuevo = models.CharField(max_length=50)
    class Meta:
        db_table = 'Sector'



class Jornada(models.Model):
    JORNA_Nombre = models.CharField(max_length=50)
    class Meta:
        db_table = 'Jornada'



class Empresa(models.Model):
    EMPRE_Tipo_Identificacion = models.CharField(max_length=50)
    EMPRE_Nombre = models.CharField(max_length=50)
    EMPRE_Identificacion = models.CharField(max_length=50)
    class Meta:
        db_table = 'Empresa'



class Centro(models.Model):
    CENTR_Nombre = models.CharField(max_length=50)
    regional = models.ForeignKey(
        Regional,
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = 'Centro'



class ProgramaFormacion(models.Model):
    PROGR_Nombre = models.CharField(max_length=50) 
    PROGR_Modalidad = models.CharField(max_length=50)
    PROGR_Tipo_Formacion = models.CharField(max_length=50)
    PROGR_Duracion = models.CharField(max_length=50)
    PROGR_Version = models.CharField(max_length=50)
    PROGR_Nivel = models.CharField(max_length=50)
    PROGR_URL = models.FileField(upload_to='ProgramaFor/', blank=True, null=True)
    sector = models.ForeignKey(
        Sector,
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = 'Programa_Formacion'



class Ficha(models.Model):
    FICHA_Identificador_Unico = models.CharField(max_length=50)
    FICHA_Fecha_Inicio = models.DateField() 
    FICHA_Fecha_Terminacion = models.DateField() 
    FICHA_Etapa = models.CharField(max_length=50)
    FICHA_Nombre_Responsable = models.CharField(max_length=50)
    centro = models.ForeignKey(
        Centro,
        on_delete = models.CASCADE
    )
    programaformacion = models.ForeignKey(
        ProgramaFormacion,
        on_delete = models.CASCADE
    )
    jornada = models.ForeignKey(
        Jornada,
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = 'Ficha'



class Ocupacion(models.Model):
    OCUPA_Nombre = models.CharField(max_length=50)
    OCUPA_Codigo_Hora = models.CharField(max_length=50)
    sector = models.ForeignKey(
        Sector,
        on_delete = models.CASCADE 
    )
    class Meta:
        db_table = 'Ocupacion'



class Convenio(models.Model):
    CONVE_Nombre = models.CharField(max_length=50)
    CONVE_Ampliacion_Cobertura = models.CharField(max_length=50)
    empresa = models.ForeignKey(
        Empresa,
        on_delete = models.CASCADE
    )
    sector = models.ForeignKey(
        Sector,
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = 'Convenio'



class ProgramaEspecial(models.Model):
    PROGE_Nombre = models.CharField(max_length=50)
    PROGE_Modalidad = models.CharField(max_length=50)
    sector = models.ForeignKey(
        Sector, 
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = 'Programa_Especial'



class Horas(models.Model):
    HORAS_Monitores = models.CharField(max_length=50)
    HORAS_Inst_Empresa = models.CharField(max_length=50)
    HORAS_Contratista_Externos = models.CharField(max_length=50)
    HORAS_Planta = models.CharField(max_length=50)
    HORAS_Total = models.CharField(max_length=50)
    ocupacion = models.ForeignKey(
        Ocupacion,
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = 'Horas'

 
class Curso(models.Model):
    CURSO_Numero = models.CharField(max_length=50)
    CURSO_Nombre = models.CharField(max_length=50)
    CURSO_Estado = models.CharField(max_length=50)
    CURSO_Tipo = models.CharField(max_length=50)
    sector = models.ForeignKey(
        Sector,
        on_delete = models.CASCADE
    )
    municipiocurso = models.ForeignKey(
        MunicipioCurso,
        on_delete = models.CASCADE
    )
    jornada = models.ForeignKey(
        Jornada,
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = 'Curso'



class Aprendiz(models.Model):
    APREN_Nombre = models.CharField(max_length=50)
    APREN_Apellido = models.CharField(max_length=50)
    APREN_Documento = models.CharField(max_length=50)
    APREN_Tipo_Documento = models.CharField(max_length=50)
    APREN_Celular = models.CharField(max_length=50)
    APREN_Estado = models.CharField(max_length=50)
    APREN_Correo = models.CharField(max_length=50)
    APREN_Foto = models.ImageField(upload_to='Aprendiz/', blank=True, null=True)
    ficha = models.ForeignKey(
        Ficha, 
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = 'Aprendiz'

class Importar(models.Model):
    importar = models.FileField(upload_to='Importar/', blank=True, null=True)
    class Meta:
        db_table = 'Importar'