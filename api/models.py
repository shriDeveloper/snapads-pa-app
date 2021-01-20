from django.db import models
class Store(models.Model):
    name = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=100,null=True)
    token = models.CharField(max_length=100,null=True)
class Settings(models.Model):
    store_token = models.CharField(max_length=100,null=True,blank=True)
    body_tag = models.CharField(max_length=100,null=True,blank=True)
    h1_tag = models.CharField(max_length=100,null=True,blank=True)
    h2_tag = models.CharField(max_length=100,null=True,blank=True)
    h3_tag = models.CharField(max_length=100,null=True,blank=True)
    h4_tag = models.CharField(max_length=100,null=True,blank=True)
    h5_tag = models.CharField(max_length=100,null=True,blank=True)
    h6_tag = models.CharField(max_length=100,null=True,blank=True)
    p_tag = models.CharField(max_length=100,null=True,blank=True)
    block_tag = models.CharField(max_length=100,null=True,blank=True)
    li_tag = models.CharField(max_length=100,null=True,blank=True)
    a_tag = models.CharField(max_length=100,null=True,blank=True)
    custom_classes = models.TextField(null=True,blank=True)
    custom_font = models.CharField(max_length=100,null=True,blank=True)
class CustomFonts(models.Model):
    store_url =   models.CharField(max_length=100,null=True,blank=True)
    font_name   = models.CharField(max_length=100,null=True,blank=True)
