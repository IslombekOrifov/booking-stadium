# Generated by Django 4.2 on 2024-02-07 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('sa', 'Site Admin'), ('so', 'Stadium Owner'), ('u', 'User')], default='u', max_length=2),
        ),
    ]