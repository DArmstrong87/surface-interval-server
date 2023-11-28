# Generated by Django 4.2.6 on 2023-11-28 05:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("surfaceintervalapi", "0005_remove_gearitem_last_serviced_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="gearset",
            old_name="weights",
            new_name="weight",
        ),
        migrations.RemoveField(
            model_name="gearset",
            name="bcd",
        ),
        migrations.RemoveField(
            model_name="gearset",
            name="boots",
        ),
        migrations.RemoveField(
            model_name="gearset",
            name="computer",
        ),
        migrations.RemoveField(
            model_name="gearset",
            name="exposure_suit",
        ),
        migrations.RemoveField(
            model_name="gearset",
            name="fins",
        ),
        migrations.RemoveField(
            model_name="gearset",
            name="mask",
        ),
        migrations.RemoveField(
            model_name="gearset",
            name="octopus",
        ),
        migrations.RemoveField(
            model_name="gearset",
            name="regulator",
        ),
        migrations.RemoveField(
            model_name="gearset",
            name="tank",
        ),
        migrations.AddField(
            model_name="gearset",
            name="gear_items",
            field=models.ManyToManyField(
                related_name="gear_sets", to="surfaceintervalapi.gearitem"
            ),
        ),
    ]
