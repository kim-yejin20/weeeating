# Generated by Django 3.1.5 on 2021-01-28 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeimage',
            name='image',
            field=models.URLField(max_length=1000),
        ),
    ]