# Generated by Django 5.0 on 2024-01-19 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_alter_application_masters_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Masters',
            new_name='Master',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='masters',
            new_name='master',
        ),
        migrations.RenameField(
            model_name='orientation',
            old_name='masters',
            new_name='master',
        ),
    ]
