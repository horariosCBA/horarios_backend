# Generated by Django 4.2.1 on 2024-08-08 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_vocero'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='fechaRegistro',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
