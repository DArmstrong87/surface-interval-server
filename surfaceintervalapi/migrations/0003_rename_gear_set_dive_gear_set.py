# Generated by Django 4.0.3 on 2022-04-18 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surfaceintervalapi', '0002_remove_diver_default_gear_set_diver_default_gear_set'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dive',
            old_name='Gear_Set',
            new_name='gear_set',
        ),
    ]