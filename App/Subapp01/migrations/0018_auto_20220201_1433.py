# Generated by Django 3.2.6 on 2022-02-01 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Subapp01', '0017_auto_20220201_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emi_data',
            name='LoanAmount',
        ),
        migrations.RemoveField(
            model_name='emi_data',
            name='creditscore',
        ),
        migrations.RemoveField(
            model_name='emi_data',
            name='monthlySalary',
        ),
        migrations.RemoveField(
            model_name='emi_data',
            name='tenure',
        ),
    ]
