# Generated by Django 4.0.3 on 2022-04-19 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surfaceintervalapi', '0007_alter_favorite_dive_dive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite_dive',
            name='dive',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='surfaceintervalapi.dive'),
        ),
    ]
