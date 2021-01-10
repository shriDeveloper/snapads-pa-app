from django.db import models
class Store(models.Model):
    name = models.CharField(max_length=100,null=True,default='')
    email = models.CharField(max_length=100,null=True,default='')
    token = models.CharField(max_length=100,null=True,default='')
class Settings(models.Model):
    store_token = models.CharField(max_length=100,null=True,default='')
    store_logo = models.CharField(max_length=100,null=True,default='')
    store_header = models.CharField(max_length=100,null=True,default='')
    store_footer = models.CharField(max_length=100,null=True,default='')