# Generated by Django 4.0.3 on 2022-04-20 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfaceintervalapi', '0009_gear_set_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gear_type',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
