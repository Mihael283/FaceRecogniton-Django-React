from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField
from django.utils.safestring import mark_safe

# Create your models here.

class Profile(models.Model):
    profile_id=models.AutoField(primary_key=True,editable=False)
    name= models.CharField(max_length = 200 , null=True, blank=True)
    surname= models.CharField(max_length = 200 , null=True, blank=True)
    id_image= models.ImageField(null=True,blank=True, default = '/No_image.png')
    selfie_image= models.ImageField(null=True,blank=True, default = '/No_image.png')
    encodings =  PickledObjectField(null=True,blank=True)

    def __str__(self):
        return self.name

