# Generated by Django 4.0.3 on 2022-04-18 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfaceintervalapi', '0005_dive_specialty_custom_specialty_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='certification_card',
            name='name',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
