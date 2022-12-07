# Generated by Django 4.1.1 on 2022-12-06 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoSennova', '0005_alter_aprendiz_apren_apellido_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Instructor'), (2, 'Administrador')], default=1, null=True),
        ),
    ]
