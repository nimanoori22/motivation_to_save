from django.db import models
from django.contrib.auth.models import User
from . management.commands.scrape import Digikala 
import json
# Create your models here.

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=250, null=False)
    img = models.CharField(max_length=250, null=True, blank=True)
    price = models.CharField(max_length=250, null=True, blank=True)
    features = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    def save(self, *args, **kwargs):

         dg = Digikala(self.url)
         self.img = dg.get_pic()
         self.price = dg.get_price()
         self.features = json.dumps(dg.get_features())
         super().save(*args, **kwargs)
         
