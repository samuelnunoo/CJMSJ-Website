# Generated by Django 2.2.2 on 2019-07-04 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190704_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='static/img/beautiful-landscape.jpg', upload_to='portraits'),
        ),
    ]
