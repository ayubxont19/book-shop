# Generated by Django 5.1.3 on 2025-02-28 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book_model',
            name='IsDeleted',
            field=models.BooleanField(default=False),
        ),
    ]
