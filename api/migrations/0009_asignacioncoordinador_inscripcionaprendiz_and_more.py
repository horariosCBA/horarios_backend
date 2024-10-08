# Generated by Django 4.2.1 on 2024-08-21 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_usuario_celular_alter_usuario_telefono'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionCoordinador',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('usuario', models.IntegerField()),
                ('Programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.programa')),
            ],
        ),
        migrations.CreateModel(
            name='InscripcionAprendiz',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('usuario', models.IntegerField()),
                ('ficha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ficha')),
            ],
        ),
        migrations.AddField(
            model_name='usuario',
            name='vocero',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Vocero',
        ),
    ]
