# Generated by Django 5.1.6 on 2025-03-04 19:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('despachos', '0001_initial'),
        ('funcionarios', '0001_initial'),
        ('novedades', '0001_initial'),
        ('tipocargos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CargosAsignados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('acuerdo', models.CharField(max_length=200)),
                ('Ofertable', models.CharField(choices=[('Si', 'Si'), ('No', 'No')], max_length=200)),
                ('estado_vacante', models.BooleanField(default=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tipocargos.tipocargo')),
                ('despacho', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='despachos.despacho')),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='funcionarios.funcionario')),
                ('novedad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='novedades.novedad')),
            ],
            options={
                'verbose_name': 'Funcionario',
                'verbose_name_plural': 'Funcionarios',
                'ordering': ['-fecha_inicio'],
            },
        ),
    ]
