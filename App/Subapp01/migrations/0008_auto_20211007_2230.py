# Generated by Django 3.0.14 on 2021-10-07 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Subapp01', '0007_faqcategory_faqtext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqtext',
            name='description',
            field=models.TextField(),
        ),
    ]
