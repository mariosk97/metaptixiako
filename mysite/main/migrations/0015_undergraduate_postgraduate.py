# Generated by Django 4.0.6 on 2023-10-17 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_theses_grade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Undergraduate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('univercity', models.CharField(max_length=150, null=True)),
                ('department', models.CharField(max_length=150, null=True)),
                ('degree_title', models.CharField(blank=True, max_length=150, null=True)),
                ('grade', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Postgraduate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('univercity', models.CharField(max_length=150, null=True)),
                ('department', models.CharField(max_length=150, null=True)),
                ('degree_title', models.CharField(blank=True, max_length=150, null=True)),
                ('grade', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
