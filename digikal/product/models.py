from django.db import models
from django.contrib.auth.models import User
from . management.commands.scrape import Digikala 
import json
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.utils.translation import ugettext_lazy as _
# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    url = models.CharField(max_length=500, null=False)
    img = models.CharField(max_length=250, null=True, blank=True)
    price = models.CharField(max_length=250, null=True, blank=True)
    features = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

         dg = Digikala(self.url)
         self.img = dg.get_pic()
         self.price = dg.get_price()
         self.features = json.dumps(dg.get_features())
         self.title = dg.get_title()
         super().save(*args, **kwargs)
         
