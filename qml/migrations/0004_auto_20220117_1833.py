# Generated by Django 3.2.4 on 2022-01-17 10:33

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qml', '0003_alter_layer_geojson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='feat_id',
        ),
        migrations.AlterField(
            model_name='feature',
            name='geometry',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
    ]
