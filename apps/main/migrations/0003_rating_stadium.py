# Generated by Django 4.2 on 2024-02-05 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_stadium_lat_alter_stadium_long'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='stadium',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='main.stadium'),
            preserve_default=False,
        ),
    ]