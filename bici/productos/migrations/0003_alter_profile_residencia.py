# Generated by Django 5.0.7 on 2024-07-21 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_profile_estado_civil_profile_residencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='residencia',
            field=models.CharField(blank=True, choices=[('chile', 'Chile'), ('argentina', 'Argentina'), ('españa', 'España'), ('colombia', 'Colombia')], max_length=255, null=True),
        ),
    ]
