from django.db import connection
from django.db import models

class PaisCurso(models.Model):
    PAISC_Nombre = models.CharField(max_length=150) 
    class Meta:
        db_table = 'PaisCurso'

