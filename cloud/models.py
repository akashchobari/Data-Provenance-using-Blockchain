from django.db import models

# Create your models here.
class meta(models.Model):
    username = models.CharField(max_length=250)
    #metadat = models.CharField(max_length=15000)
    metadata = models.FileField(null=True ,blank=True)
class TodoModel(models.Model):
    task = models.CharField(max_length = 20)
    

    
