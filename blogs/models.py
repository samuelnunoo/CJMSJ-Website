from django.db import models
from django.urls import reverse
from django.shortcuts import  redirect
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django import template
from ckeditor.fields import RichTextField
from users.models import Profile
from django.conf import settings
from users.models import Profile
register = template.Library()
# Create your models here.



class Post(models.Model):
    Title=models.CharField(max_length=100)
    Created=models.DateTimeField(auto_now_add=True)
    Image=models.ImageField(upload_to='pictures/', default='img/beautiful-landscape.jpg')
    Content=RichTextField()
    Approved=models.BooleanField(default=False)
    Description=models.TextField(default='This is a sample Description',max_length=120)
    Featured=models.BooleanField(default=False)
    Author=models.ManyToManyField(Profile)
    Rejected=models.BooleanField(default=False)

    def page_url(self):
        print(reverse('blogs:page',kwargs={'id':self.id}))
        return reverse('blogs:page',kwargs={'id':self.id})


    def review_url(self):
        return reverse('blogs:review_article',kwargs={'id':self.id})


    def preview_url(self):
        return reverse('blogs:preview_article', kwargs={'id': self.id})

class StaticItems(models.Model):
    Image=models.ImageField(upload_to='pictures/')
    name=models.CharField(max_length=20,default=None)


