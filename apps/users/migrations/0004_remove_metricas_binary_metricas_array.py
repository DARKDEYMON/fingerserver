# Generated by Django 4.1.7 on 2023-04-09 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_metricas_binary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metricas',
            name='binary',
        ),
        migrations.AddField(
            model_name='metricas',
            name='array',
            field=models.TextField(blank=True, null=True),
        ),
    ]
