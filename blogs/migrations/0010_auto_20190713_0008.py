# Generated by Django 2.2.2 on 2019-07-13 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0009_auto_20190712_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Description',
            field=models.TextField(default='This is a sample Description', max_length=120),
        ),
    ]
