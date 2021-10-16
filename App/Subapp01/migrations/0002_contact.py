# Generated by Django 3.0.14 on 2021-06-24 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Subapp01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Firstname', models.CharField(max_length=100)),
                ('Lastname', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=100)),
                ('Phone', models.EmailField(max_length=100)),
                ('Loan', models.IntegerField(max_length=100)),
                ('Bank', models.CharField(max_length=100)),
            ],
        ),
    ]
