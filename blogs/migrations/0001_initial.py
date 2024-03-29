# Generated by Django 2.2.2 on 2019-06-24 01:10

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=40)),
                ('Created', models.DateTimeField(auto_now_add=True)),
                ('Image', models.ImageField(upload_to='pictures/')),
                ('Content', tinymce.models.HTMLField(default='testing')),
                ('Approved', models.BooleanField(default=False)),
                ('Description', models.TextField(default='This is a sample Description')),
                ('Featured', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StaticItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='pictures/')),
                ('name', models.CharField(default=None, max_length=20)),
            ],
        ),
    ]
