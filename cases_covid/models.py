from django.db import models

# Create your models here.
class cases_Ecuador_covid(models.Model):
    fecha = models.DateTimeField()
    total_casos = models.CharField(max_length=100)