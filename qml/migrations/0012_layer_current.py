# Generated by Django 3.2.4 on 2022-01-18 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qml', '0011_auto_20220118_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='current',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
