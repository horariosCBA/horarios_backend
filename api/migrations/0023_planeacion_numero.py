# Generated by Django 4.2.1 on 2024-09-23 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_rename_usuario_asignacionaula_programa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='planeacion',
            name='numero',
            field=models.IntegerField(default=0),
        ),
    ]
