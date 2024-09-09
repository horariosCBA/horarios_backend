# Generated by Django 4.2.1 on 2024-08-28 01:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_usuario_rol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Planeacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('duracionPresencial', models.IntegerField(blank=True, null=True)),
                ('duracionVirtual', models.IntegerField(blank=True, null=True)),
                ('duracionTotal', models.IntegerField()),
                ('resultadoAprendizaje', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.resultadoaprendizaje')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('planeacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.planeacion')),
            ],
        ),
        migrations.CreateModel(
            name='Programacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('trimestre', models.IntegerField()),
                ('ficha', models.IntegerField()),
                ('diasAsignados', models.IntegerField()),
                ('planeacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.planeacion')),
            ],
        ),
        migrations.CreateModel(
            name='Tematica',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('planeacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.planeacion')),
            ],
        ),
        migrations.RenameField(
            model_name='mensaje',
            old_name='fecha',
            new_name='fechaEnviado',
        ),
        migrations.RemoveField(
            model_name='competencia',
            name='criterioEvaluacion',
        ),
        migrations.RemoveField(
            model_name='horario',
            name='planeacionPedagogica',
        ),
        migrations.AddField(
            model_name='mensaje',
            name='fechaRecibido',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='enLinea',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='PlaneacionPedagogica',
        ),
        migrations.AddField(
            model_name='programacion',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.usuario'),
        ),
        migrations.AddField(
            model_name='horario',
            name='programacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.programacion'),
        ),
    ]
