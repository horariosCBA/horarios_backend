# Generated by Django 4.2.1 on 2024-10-05 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_alter_programa_duracionproductiva_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='planeacion',
            old_name='duracionPresencial',
            new_name='trabajoAutonomo',
        ),
        migrations.RenameField(
            model_name='planeacion',
            old_name='duracionVirtual',
            new_name='trabajoDirecto',
        ),
        migrations.RemoveField(
            model_name='ficha',
            name='modalidad',
        ),
        migrations.RemoveField(
            model_name='ficha',
            name='tipoOferta',
        ),
        migrations.AddField(
            model_name='programa',
            name='modalidad',
            field=models.CharField(choices=[('Presencial', 'Presencial'), ('Virtual', 'Virtual'), ('A Distancia', 'A Distancia'), ('Mixta (B-Learning)', 'Mixta (B-Learning)'), ('Contrato de Aprendizaje', 'Contrato de Aprendizaje'), ('Articulación con la Media', 'Articulación con la Media'), ('Escuela-Taller', 'Escuela-Taller')], default='Presencial', max_length=100),
        ),
        migrations.AddField(
            model_name='programa',
            name='tipoOferta',
            field=models.CharField(choices=[('Oferta Abierta', 'Oferta Abierta'), ('Colegio', 'Colegio'), ('Empresa', 'Empresa'), ('Institución', 'Institución'), ('Programa Especial', 'Programa Especial'), ('Educación Continua', 'Educación Continua'), ('Cadena de Formación', 'Cadena de Formación')], default='Oferta Abierta', max_length=100),
        ),
        migrations.AlterField(
            model_name='planeacion',
            name='diasRecomendados',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=2),
        ),
        migrations.AlterField(
            model_name='programacion',
            name='diasAsignados',
            field=models.DecimalField(decimal_places=0, max_digits=2),
        ),
    ]
