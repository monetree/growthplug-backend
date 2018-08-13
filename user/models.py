from django.db import models

class PostData(models.Model):
    title   = models.CharField(max_length=60,null=True,blank=True,default="default name")
    desc = models.CharField(max_length=60,null=True,blank=True,default='default desc')
