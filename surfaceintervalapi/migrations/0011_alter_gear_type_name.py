# Generated by Django 4.0.3 on 2022-04-20 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfaceintervalapi', '0010_alter_gear_type_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gear_type',
            name='name',
            field=models.CharField(default='Type', max_length=50),
        ),
    ]