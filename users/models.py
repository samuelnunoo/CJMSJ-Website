from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,

        )
        user.is_admin = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class QuerySet(models.QuerySet):
    def name(self):
        return


class Profile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField(default='An amazing person from an amazing place!')
    image = models.ImageField(default='pictures/default.jpg')
    first_name = models.CharField(max_length=24,blank=True)
    last_name = models.CharField(max_length=24,blank=True)
    title=models.CharField(default='User',max_length=24)
    staff=models.BooleanField(default=False)

    #For Filtering of Users
    complete = models.BooleanField(default=False)



    def page_url(self):
        #print("THIS IS PRINTING",reverse('users:pages',kwargs={'id':self.id}))
        return reverse('users:pages',kwargs={'id':self.id})


    def name(self):
        return "%s %s" %(self.first_name,self.last_name)

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name,last_name=self.last_name)


@receiver(post_save,sender=Account)
def update_user_profile(sender,instance,created,**kwargs):
    user=instance
    if created:
        profile=Profile(user=user)
        profile.email_confirmed = True
        profile.save()


# Create your models here.
