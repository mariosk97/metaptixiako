# Generated by Django 4.0.6 on 2022-08-23 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_applied',
            field=models.BooleanField(default=False),
        ),
    ]
