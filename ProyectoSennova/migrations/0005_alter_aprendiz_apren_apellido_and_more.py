# Generated by Django 4.1.1 on 2022-12-06 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoSennova', '0004_alter_aprendiz_apren_celular_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aprendiz',
            name='APREN_Apellido',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='aprendiz',
            name='APREN_Celular',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='aprendiz',
            name='APREN_Correo',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='aprendiz',
            name='APREN_Documento',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='aprendiz',
            name='APREN_Estado',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='aprendiz',
            name='APREN_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='aprendiz',
            name='APREN_Tipo_Documento',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='centro',
            name='CENTR_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='CONT_Estado_Aprendiz',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='CONT_Estado_Contrato',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='convenio',
            name='CONVE_Ampliacion_Cobertura',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='convenio',
            name='CONVE_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='curso',
            name='CURSO_Estado',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='curso',
            name='CURSO_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='curso',
            name='CURSO_Numero',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='curso',
            name='CURSO_Tipo',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='departamentocurso',
            name='DEPAR_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='EMPRE_Identificacion',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='EMPRE_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='EMPRE_Tipo_Identificacion',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ficha',
            name='FICHA_Etapa',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ficha',
            name='FICHA_Identificador_Unico',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ficha',
            name='FICHA_Nombre_Responsable',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='horas',
            name='HORAS_Contratista_Externos',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='horas',
            name='HORAS_Inst_Empresa',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='horas',
            name='HORAS_Monitores',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='horas',
            name='HORAS_Planta',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='horas',
            name='HORAS_Total',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='jornada',
            name='JORNA_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='municipiocurso',
            name='MUNIC_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ocupacion',
            name='OCUPA_Codigo_Hora',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ocupacion',
            name='OCUPA_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='paiscurso',
            name='PAISC_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='programaespecial',
            name='PROGE_Modalidad',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='programaespecial',
            name='PROGE_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='programaformacion',
            name='PROGR_Duracion',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='programaformacion',
            name='PROGR_Modalidad',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='programaformacion',
            name='PROGR_Nivel',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='programaformacion',
            name='PROGR_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='programaformacion',
            name='PROGR_Tipo_Formacion',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='programaformacion',
            name='PROGR_Version',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='regional',
            name='REGIO_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='sector',
            name='SECTO_Nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='sector',
            name='SECTO_NombreNuevo',
            field=models.CharField(max_length=100),
        ),
    ]
