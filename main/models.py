from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Found_img(models.Model):  
    
    """
    Found_img:-                     table name
    user,image......:-              column name
    ImageField, Charfield.....:-    datatype of column
    ForeignKey:-                    Connected to User table with foregin key (User table is inbuilt)
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='image')
    name = models.CharField(max_length=100 , blank=True, null=True)
    im_class = models.IntegerField(blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    box_x1 = models.FloatField(blank=True, null=True)
    box_x2 = models.FloatField(blank=True, null=True)
    box_y1 = models.FloatField(blank=True, null=True)
    box_y2 = models.FloatField(blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.user.username) + " " + str(self.name) # Name to display in admin pannel
    
    
    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile', verbose_name='profile')
    phone = models.CharField(max_length=100)
    
    def __str__(self) :
        return self.user.username
        