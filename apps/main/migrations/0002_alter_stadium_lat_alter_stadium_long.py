# Generated by Django 4.2 on 2024-02-05 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stadium',
            name='lat',
            field=models.DecimalField(decimal_places=18, max_digits=22),
        ),
        migrations.AlterField(
            model_name='stadium',
            name='long',
            field=models.DecimalField(decimal_places=18, max_digits=22),
        ),
    ]
