# Generated by Django 2.2.2 on 2019-07-04 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190704_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='pictures/beautiful-landscape.jpg', upload_to=''),
        ),
    ]
