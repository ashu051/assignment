from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    
    
class Main(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='aadmi')
    def __str__(self):
        return str(self.id)
    
    
class Advisor(models.Model):
    khiladi = models.ForeignKey(Main, on_delete=models.CASCADE,related_name='aadmi')
    booking_time = models.DateTimeField(auto_now=True)
    advisor_name = models.CharField(max_length=20)
    advisor_image=models.ImageField(upload_to='bookimages')
    def __str__(self):
        return str(self.id)
