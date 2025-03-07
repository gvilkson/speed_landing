# Generated by Django 5.0.6 on 2024-05-16 00:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_accesslog_user_agent'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesslog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accesslog',
            name='user_agent',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
