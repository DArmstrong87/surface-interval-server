# Generated by Django 4.2.6 on 2023-11-10 22:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("surfaceintervalapi", "0002_alter_dive_gear_set"),
    ]

    operations = [
        migrations.RenameField(
            model_name="dive",
            old_name="country_state",
            new_name="location",
        ),
    ]
