# Generated by Django 3.2.4 on 2022-01-18 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qml', '0007_layerhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layerhistory',
            name='layer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='layerhistory_history', to='qml.layer'),
        ),
    ]