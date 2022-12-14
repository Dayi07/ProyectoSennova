from pyexpat import model
from tkinter import CASCADE
from django.db import connection, models, migrations
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    INSTRUCTOR = 1
    ADMINISTRADOR = 2
      
    ROLE_CHOICES = (
      (INSTRUCTOR, 'Instructor'),
      (ADMINISTRADOR, 'Administrador'),
    )    
    foto = models.ImageField(upload_to='User/', blank=True, null=True, default='User/user.jpg')
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=1)


class PaisCurso(models.Model):
    PAISC_Nombre = models.CharField(max_length=100) 
    class Meta:
        db_table = 'Pais_Curso'


 
class DepartamentoCurso(models.Model):
    DEPAR_Nombre = models.CharField(max_length=100)
    paiscurso = models.ForeignKey(
        PaisCurso, 
        on_delete=models.CASCADE, 
        )  
    class Meta:
        db_table = 'Departamento_Curso'
    


class MunicipioCurso(models.Model):
    MUNIC_Nombre = models.CharField(max_length=100)
    departamentocurso = models.ForeignKey(
        DepartamentoCurso,
        on_delete = models.CASCADE,
    )
    class Meta:
        db_table = 'Municipio_Curso'



class Regional(models.Model):
    REGIO_Nombre = models.CharField(max_length=100)

    migrations.RunSQL('INSERT INTO `Regional`(`id`, `REGIO_Nombre`) VALUES (1, "None");')

    class Meta:
        db_table = 'Regional'
    


class Sector(models.Model):
    SECTO_Nombre = models.CharField(max_length=100)
    SECTO_NombreNuevo = models.CharField(max_length=100)

    migrations.RunSQL('INSERT INTO `Sector`(`id`, `SECTO_Nombre`, `SECTO_NombreNuevo`) VALUES (1, "None", "None");')

    class Meta:
        db_table = 'Sector'



class Jornada(models.Model):
    JORNA_Nombre = models.CharField(max_length=100)

    migrations.RunSQL('INSERT INTO `Jornada`(`id`, `JORNA_Nombre`) VALUES (1, "None");')

    class Meta:
        db_table = 'Jornada'



class Empresa(models.Model):
    EMPRE_Tipo_Identificacion = models.CharField(max_length=100)
    EMPRE_Nombre = models.CharField(max_length=100)
    EMPRE_Identificacion = models.CharField(max_length=100)
    class Meta:
        db_table = 'Empresa'



class Centro(models.Model):
    CENTR_Nombre = models.CharField(max_length=100)
    regional = models.ForeignKey(
        Regional,
        on_delete = models.CASCADE
    )

    migrations.RunSQL('INSERT INTO `Centro`(`id`, `CENTR_Nombre`, `regional_id`) VALUES (1, "None", 1);')

    class Meta:
        db_table = 'Centro'



class ProgramaFormacion(models.Model):
    PROGR_Nombre = models.CharField(max_length=100) 
    PROGR_Modalidad = models.CharField(max_length=100)
    PROGR_Tipo_Formacion = models.CharField(max_length=100)
    PROGR_Duracion = models.CharField(max_length=100)
    PROGR_Version = models.CharField(max_length=100)
    PROGR_Nivel = models.CharField(max_length=100)
    PROGR_URL = models.FileField(upload_to='ProgramaFor/', blank=True, null=True)
    sector = models.ForeignKey(
        Sector,
        on_delete = models.CASCADE
    )

    migrations.RunSQL('INSERT INTO Programa_Formacion(`id`, `PROGR_Nombre`, `PROGR_Modalidad`, `PROGR_Tipo_Formacion`, `PROGR_Duracion`, `PROGR_Version`, `PROGR_Nivel`, `PROGR_URL`,  `sector_id`) VALUES (1, "None", "None", "None", "None", "None", "None", "None", 1);')

    class Meta:
        db_table = 'Programa_Formacion'



class Ficha(models.Model):
    FICHA_Identificador_Unico = models.CharField(max_length=100)
    FICHA_Fecha_Inicio = models.DateField() 
    FICHA_Fecha_Terminacion = models.DateField() 
    FICHA_Etapa = models.CharField(max_length=100)
    FICHA_Nombre_Responsable = models.CharField(max_length=100)
    FICHA_Actualizacion_Carga = models.DateField() 
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
    OCUPA_Nombre = models.CharField(max_length=100)
    OCUPA_Codigo_Hora = models.CharField(max_length=100)
    sector = models.ForeignKey(
        Sector,
        on_delete = models.CASCADE 
    )
    class Meta:
        db_table = 'Ocupacion'



class Convenio(models.Model):
    CONVE_Nombre = models.CharField(max_length=100)
    CONVE_Ampliacion_Cobertura = models.CharField(max_length=100)
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
    PROGE_Nombre = models.CharField(max_length=100)
    PROGE_Modalidad = models.CharField(max_length=100)
    sector = models.ForeignKey(
        Sector, 
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = 'Programa_Especial'



class Horas(models.Model):
    HORAS_Monitores = models.CharField(max_length=100)
    HORAS_Inst_Empresa = models.CharField(max_length=100)
    HORAS_Contratista_Externos = models.CharField(max_length=100)
    HORAS_Planta = models.CharField(max_length=100)
    HORAS_Total = models.CharField(max_length=100)
    ocupacion = models.ForeignKey(
        Ocupacion,
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = 'Horas'

 
class Curso(models.Model):
    CURSO_Numero = models.CharField(max_length=100)
    CURSO_Nombre = models.CharField(max_length=100)
    CURSO_Estado = models.CharField(max_length=100)
    CURSO_Tipo = models.CharField(max_length=100)
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
    APREN_Nombre = models.CharField(max_length=100)
    APREN_Apellido = models.CharField(max_length=100)
    APREN_Documento = models.CharField(max_length=100)
    APREN_Tipo_Documento = models.CharField(max_length=100)
    APREN_Celular = models.CharField(max_length=100)
    APREN_Estado = models.CharField(max_length=100)
    APREN_Correo = models.CharField(max_length=100)
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



class Contrato(models.Model):
    CONT_Fecha_Creacion = models.DateField()
    CONT_Fecha_Inicio = models.DateField()
    CONT_Fecha_Terminacion = models.DateField()
    CONT_Estado_Aprendiz = models.CharField(max_length=100)
    CONT_Estado_Contrato = models.CharField(max_length=100)
    aprendiz = models.ForeignKey(
        Aprendiz,
        on_delete = models.CASCADE
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete = models.CASCADE
    )
    class Meta:
        db_table = 'Contrato'

