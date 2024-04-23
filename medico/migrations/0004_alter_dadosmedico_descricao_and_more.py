# Generated by Django 4.2.11 on 2024-04-22 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0003_datasabertas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dadosmedico',
            name='descricao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosmedico',
            name='especialidade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='medico.especialidades'),
        ),
    ]
