# Generated by Django 4.2.13 on 2024-05-12 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='institute',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='project',
            name='university',
            field=models.CharField(default='', max_length=150, null=True),
        ),
    ]
