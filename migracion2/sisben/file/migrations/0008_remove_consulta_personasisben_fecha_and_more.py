# Generated by Django 4.1.7 on 2023-03-09 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0007_rename_tipodocumento_id_consulta_personasisben_tipodocumento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consulta_personasisben',
            name='fecha',
        ),
        migrations.RemoveField(
            model_name='consulta_personasisben',
            name='fechaentregatarjeta',
        ),
        migrations.RemoveField(
            model_name='consulta_personasisben',
            name='fecharegsdm',
        ),
    ]
