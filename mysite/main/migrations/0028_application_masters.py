# Generated by Django 5.0 on 2024-01-18 14:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_remove_masters_orientation_orientation_masters'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='masters',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.masters'),
        ),
    ]