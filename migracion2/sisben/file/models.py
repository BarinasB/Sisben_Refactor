from django.db import models

DOCUMENTS_CHOICES = (
    (0, "No tiene"),
    (1, "Cedula de Ciudadania"),
    (2, "Tarjeta de Identidad"),
    (3, "Cedula de Extranjeria"),
    (4, "Registro Civil"),
)

class tmp_consulta_personasisben(models.Model):
    id = models.IntegerField(null=True, blank=True)
    ficha = models.TextField(null=True, blank=True)
    tipodocumento_id = models.IntegerField(null=True, db_column='tipodocumento_id', blank=True)
    documen = models.TextField(null=True, blank=True)
    ape1 = models.CharField(max_length=135, blank=True)
    ape2 = models.CharField(max_length=135, blank=True)
    nom1 = models.CharField(max_length=135, blank=True)
    nom2 = models.CharField(max_length=135, blank=True)
    sexo = models.IntegerField(null=True, blank=True)
    tiponovedad_id = models.IntegerField(null=True, db_column='tiponovedad_id', blank=True) 
    placa = models.CharField(max_length=135, db_column='Placa', blank=True) 
    fechanto = models.DateField(null=True, blank=True)
    edad = models.IntegerField(null=True, db_column='Edad', blank=True)
    nombarrio = models.CharField(max_length=45, blank=True)
    direccion = models.CharField(max_length=45, blank=True)
    telefono = models.CharField(max_length=45, blank=True)
    comuna = models.CharField(max_length=45, blank=True)
    puntaje_sisbn = models.CharField(max_length=45, blank=True) 
    primak = models.AutoField( primary_key=True)
   
    
   
    class Meta:
        db_table = u'tmp_consulta_personasisben'


class consulta_personasisben(models.Model):
    
    id = models.AutoField( primary_key=True)
    ficha = models.TextField(null=True, blank=True)
    tipodocumento = models.ForeignKey('consulta_tipodocumento',null=True, on_delete=models.CASCADE)
    documen = models.CharField(max_length=36, blank=True)
    ape1 = models.CharField(max_length=135, blank=True)
    ape2 = models.CharField(max_length=135, blank=True)
    nom1 = models.CharField(max_length=135, blank=True)
    nom2 = models.CharField(max_length=135, blank=True)
    sexo = models.IntegerField(null=True, blank=True)
    tiponovedad = models.ForeignKey('consulta_tipoNovedad',null=True, on_delete=models.CASCADE) 
    placa = models.CharField(max_length=135, db_column='Placa', blank=True) 
    fechanto = models.DateField(null=True, blank=True)
    edad = models.IntegerField(null=True, db_column='Edad', blank=True) 
    nombarrio = models.CharField(max_length=45, blank=True) 
    direccion = models.CharField(max_length=45, blank=True)
    telefono = models.CharField(max_length=45, blank=True)
    comuna = models.CharField(max_length=45, blank=True)
    primak = models.IntegerField(null=True, blank=True) 
    
    
    class Meta:
        db_table = u'consulta_personasisben'

class eliminar(models.Model):
    documen = models.CharField(max_length=36, blank=True)
    tipodoc = models.IntegerField(blank=True)
    class Meta:
        db_table = u'eliminar'
        unique_together = ("tipodoc", "documen")

class Consulta_tipodocumento (models.Model):
    id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=36, blank=True)
    abrev = models.CharField(max_length=24, blank=True)
    class Meta:
        db_table = u'Consulta_tipodocumento'

class Consulta_tipoNovedad(models.Model):
    idtiponovedad = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=36, blank=True)
    
    class Meta:
        db_table = u'Consulta_tiponovedad'

