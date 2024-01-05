# Generated by Django 4.0.6 on 2023-12-20 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_postgraduate_isdeleted_undergraduate_isdeleted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postgraduate',
            old_name='isDeleted',
            new_name='is_deleted',
        ),
        migrations.RenameField(
            model_name='undergraduate',
            old_name='isDeleted',
            new_name='is_deleted',
        ),
        migrations.AlterField(
            model_name='postgraduate',
            name='univercity',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='postgraduate',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='undergraduate',
            name='univercity',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='undergraduate',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
