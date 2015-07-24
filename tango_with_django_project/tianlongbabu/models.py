#-*- coding: UTF-8 -*- 

from django.db import models

# Create your models here.

class Chapter(models.Model):
    sequence=models.IntegerField()
    chapter=models.CharField(max_length=128)
    name=models.CharField(max_length=128)
    title=models.CharField(max_length=128)
    context=models.TextField()
    
    def __unicode__(self):
        return self.chapter+':'+self.name
    
