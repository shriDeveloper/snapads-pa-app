from django.db import models
class Store(models.Model):
    name = models.CharField(max_length=100,null=True,default='')
    email = models.CharField(max_length=100,null=True,default='')
    token = models.CharField(max_length=100,null=True,default='')
class Settings(models.Model):
    store_token = models.CharField(max_length=100,null=True,default='',blank=True)
    body_tag = models.CharField(max_length=100,null=True,default='',blank=True)
    h1_tag = models.CharField(max_length=100,null=True,default='',blank=True)
    h2_tag = models.CharField(max_length=100,null=True,default='',blank=True)
    h3_tag = models.CharField(max_length=100,null=True,default='',blank=True)
    h4_tag = models.CharField(max_length=100,null=True,default='',blank=True)
    h5_tag = models.CharField(max_length=100,null=True,default='',blank=True)
    h6_tag = models.CharField(max_length=100,null=True,default='',blank=True)
    p_tag = models.CharField(max_length=100,null=True,default='',blank=True)
    block_tag = models.CharField(max_length=100,null=True,default='',blank=True)
    li_tag = models.CharField(max_length=100,null=True,default='',blank=True)
    a_tag = models.CharField(max_length=100,null=True,default='',blank=True)
class CustomFonts(models.Model):
	store_url =   models.CharField(max_length=100,null=True,default='',blank=True)
	font_name   = models.CharField(max_length=100,null=True,default='',blank=True)