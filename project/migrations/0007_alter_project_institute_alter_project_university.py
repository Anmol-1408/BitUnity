# Generated by Django 4.2.13 on 2024-05-16 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_project_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='institute',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='project',
            name='university',
            field=models.CharField(max_length=150, null=True),
        ),
    ]