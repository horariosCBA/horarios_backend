# Generated by Django 4.2.1 on 2024-08-04 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(blank=True, choices=[('Instructor', 'Instructor'), ('Aprendiz', 'Aprendiz'), ('Administrador', 'Administrador')], default='Aprendiz', max_length=15, null=True),
        ),
    ]
