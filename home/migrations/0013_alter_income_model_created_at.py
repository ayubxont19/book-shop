# Generated by Django 5.1.3 on 2025-04-11 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_delete_trash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income_model',
            name='created_at',
            field=models.DateTimeField(verbose_name='sanasi'),
        ),
    ]
