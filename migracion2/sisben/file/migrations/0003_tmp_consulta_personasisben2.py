# Generated by Django 4.1.7 on 2023-03-09 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0002_remove_tmp_consulta_personasisben_fecha_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='tmp_consulta_personasisben2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ids', models.IntegerField(blank=True, null=True)),
                ('ficha', models.TextField(blank=True, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('fecharegsdm', models.DateField(blank=True, db_column='FechaRegSDM', null=True)),
                ('tipodocumento_id', models.IntegerField(blank=True, db_column='tipodocumento_id', null=True)),
                ('documen', models.TextField(blank=True, null=True)),
                ('ape1', models.CharField(blank=True, max_length=135)),
                ('ape2', models.CharField(blank=True, max_length=135)),
                ('nom1', models.CharField(blank=True, max_length=135)),
                ('nom2', models.CharField(blank=True, max_length=135)),
                ('sexo', models.IntegerField(blank=True, null=True)),
                ('tiponovedad_id', models.IntegerField(blank=True, db_column='tiponovedad_id', null=True)),
                ('placa', models.CharField(blank=True, db_column='Placa', max_length=135)),
                ('fechanto', models.DateField(blank=True, null=True)),
                ('edad', models.IntegerField(blank=True, db_column='Edad', null=True)),
                ('fechaentregatarjeta', models.DateField(blank=True, db_column='fechaEntregaTarjeta', db_index=True, null=True)),
                ('nombarrio', models.CharField(blank=True, max_length=45)),
                ('direccion', models.CharField(blank=True, max_length=45)),
                ('telefono', models.CharField(blank=True, max_length=45)),
                ('comuna', models.CharField(blank=True, max_length=45)),
            ],
        ),
    ]
