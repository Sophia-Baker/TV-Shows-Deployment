# Generated by Django 2.2 on 2021-05-23 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows_app', '0003_auto_20210522_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]