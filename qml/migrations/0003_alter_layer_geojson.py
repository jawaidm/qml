# Generated by Django 3.2.4 on 2022-01-17 10:25

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qml', '0002_feature_layer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layer',
            name='geojson',
            field=django.contrib.postgres.fields.jsonb.JSONField(verbose_name='Layer GeoJSON'),
        ),
    ]