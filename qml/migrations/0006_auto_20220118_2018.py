# Generated by Django 3.2.4 on 2022-01-18 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qml', '0005_alter_feature_layer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dpawregion',
            old_name='feat_id',
            new_name='fid',
        ),
        migrations.RemoveField(
            model_name='layer',
            name='srid',
        ),
        migrations.AlterField(
            model_name='feature',
            name='layer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_features', to='qml.layer'),
        ),
    ]