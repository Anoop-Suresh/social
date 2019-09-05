from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name= models.CharField(max_length=250,blank=True)
    Bio= models.TextField(max_length=500, blank=True)
    Age=models.IntegerField(blank=True)
    Phone = models.IntegerField(default=0,null=True)
    Image = models.FileField(blank=True, upload_to='media/images/')


    def __str__(self):
        return self.Name