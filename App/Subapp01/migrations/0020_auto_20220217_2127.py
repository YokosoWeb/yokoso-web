# Generated by Django 3.2.6 on 2022-02-17 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Subapp01', '0019_auto_20220217_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emi_data',
            name='ongoingemi',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emi_data',
            name='salary',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emi_data',
            name='tenure',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
