# Generated by Django 4.1.7 on 2023-03-09 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0005_rename_tipodocumento_id_consulta_personasisben_tipodocumento_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='tmp_consulta_personasisben2',
        ),
        migrations.RenameField(
            model_name='consulta_personasisben',
            old_name='tipodocumento',
            new_name='tipodocumento_id',
        ),
        migrations.RenameField(
            model_name='consulta_personasisben',
            old_name='tiponovedad',
            new_name='tiponovedad_od',
        ),
    ]
