# Generated by Django 4.0.6 on 2023-12-13 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_foreign_language_grade_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='postgraduate',
            name='isDeleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='undergraduate',
            name='isDeleted',
            field=models.BooleanField(default=False),
        ),
    ]
