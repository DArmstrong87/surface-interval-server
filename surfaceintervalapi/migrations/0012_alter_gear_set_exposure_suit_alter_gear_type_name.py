# Generated by Django 4.0.3 on 2022-04-20 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surfaceintervalapi', '0011_alter_gear_type_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gear_set',
            name='exposure_suit',
            field=models.ForeignKey(blank=True, limit_choices_to={'gear_type__name': 'Exposure suit'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Exposure_Suit', to='surfaceintervalapi.gear_item'),
        ),
        migrations.AlterField(
            model_name='gear_type',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
